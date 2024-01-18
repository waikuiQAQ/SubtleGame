from Client.task import Task
from narupa.app import NarupaImdClient
import time
from additional_functions import write_to_shared_state


class Trial(Task):

    task_type = "trials"
    trial_answer_key = 'Player.TrialAnswer'
    correct_answer = None
    answer_correct = False

    def __init__(self, client: NarupaImdClient, simulation_indices: list, simulation_names: list):

        super().__init__(client=client, simulation_indices=simulation_indices)

        self.sim_names = simulation_names

    def _run_logic_for_specific_task(self):

        super()._run_logic_for_specific_task()

        self._run_single_trial()

    def _calculate_correct_answer(self, index: int = 0):
        """
        Logs the correct answer for the current trial. If the molecules are identical the correct answer will be None,
        else the correct answer is the most rigid molecule.
        """
        # Get multiplier
        multiplier = float(self.sim_names[index].removesuffix(".xml").split("_")[3].strip())

        # Molecules are identical, there is no correct answer
        if multiplier == 1:
            return

        # Get residue for modified molecule
        modified_molecule = self.sim_names[index].split("_")[2].strip()

        # The modified molecule is harder
        if multiplier > 1:
            self.correct_answer = modified_molecule

        # The reference molecule is harder, correct answer is the other one
        else:
            if modified_molecule == 'A':
                self.correct_answer = 'B'
            else:
                self.correct_answer = 'A'

    def _run_single_trial(self):

        self._calculate_correct_answer()

        self._run_simulation()

        self._wait_for_player_to_answer()

    def _run_simulation(self):

        # give the player 10 second to interact with the molecule
        time.sleep(1)

        # update shared state
        write_to_shared_state(self.client, "trials-timer", "finished")

        # pause simulation
        self.client.run_pause()

    def _wait_for_player_to_answer(self):

        while True:

            # check if player has logged an answer and break loop if they have
            try:
                current_val = self.client.latest_multiplayer_values[self.trial_answer_key]

                if current_val is not None:

                    if self.correct_answer is None:
                        was_answer_correct = "None"
                        print("No correct answer, so doesn't matter!")

                    elif current_val == self.correct_answer:
                        was_answer_correct = True
                        print("correct answer!")

                    else:
                        was_answer_correct = False
                        print("Incorrect answer :(")

                    write_to_shared_state(self.client, "trials-answer", was_answer_correct)
                    break

            # If no answer has been logged yet, wait for a bit before trying again
            except KeyError:
                time.sleep(1 / 30)

        # Remove answer once it has been received, ready for the next trial or the end of the trials
        self.client.remove_shared_value(self.trial_answer_key)

    def _update_visualisations(self):

        # Clear current selections
        self.client.clear_selections()

        # Set colour of buckyball A
        buckyball_A = self.client.create_selection("BUC_A", list(range(0, 60)))
        buckyball_A.remove()
        with buckyball_A.modify() as selection:
            selection.renderer = \
                {'render': 'ball and stick',
                 'color': 'green'
                 }

        # Set colour of buckyball B
        buckyball_B = self.client.create_selection("BUC_B", list(range(60, 120)))
        buckyball_B.remove()
        with buckyball_B.modify() as selection:
            selection.renderer = \
                {'render': 'ball and stick',
                 'color': 'cornflowerblue'
                 }
