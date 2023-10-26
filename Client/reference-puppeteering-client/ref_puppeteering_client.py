from narupa.app import NarupaImdClient
import random
import time
from ref_narupa_knot_pull_client import RefNarupaknotpullclient
from ref_preparing_game import ref_get_order_of_tasks, ref_randomise_order_of_trials
from ref_nanotube_task import ref_check_if_point_is_inside_shape, ref_get_closest_end
import numpy as np


class RefPuppeteeringClient:
    """ This is the puppeteer for the Subtle Game. It is the interface between the Rust server, Unity, and any required
     packages. """

    def __init__(self, number_of_trial_repeats: int = 2):

        # General setup.
        self.current_interaction_mode = None
        self.current_task_index = None
        self.current_task_status = None
        self.current_task_type = None

        # Prepare randomised variables.
        # self.order_of_tasks = get_order_of_tasks()
        self.order_of_tasks = ['P1']
        self.order_of_interaction_modes = random.sample(['hands', 'controllers'], 2)

        # Nanotube task.
        self.was_methane_in_nanotube = False
        self.is_methane_in_nanotube = False
        self.methane_end_of_entry = None

        # Knot-tying task.
        self.knot_pull_client = None

        # Psychophysics trials task.
        self.num_trial_repeats = number_of_trial_repeats

        # Connect to a local server (for now).
        self.narupa_client = NarupaImdClient.autoconnect()
        self.narupa_client.subscribe_multiplayer()
        self.narupa_client.subscribe_to_frames()
        self.narupa_client.update_available_commands()

        # Get simulation indices from server.
        simulations = self.narupa_client.run_command('playback/list')
        self.nanotube_index = [idx for idx, s in enumerate(simulations['simulations']) if 'nanotube' in s]
        self.alanine_index = [idx for idx, s in enumerate(simulations['simulations']) if 'alanine' in s]
        self.buckyball_indices = [idx for idx, s in enumerate(simulations['simulations']) if 'buckyball' in s]

    def start_game(self):
        """ Handles the game logic for moving through the tasks. """

        # Loop through tasks.
        for task in self.order_of_tasks:

            # Currently in Section 1 of the game.
            if '1' in task:
                self.narupa_client.set_shared_value('current section', 0)
                self.current_interaction_mode = self.order_of_interaction_modes[0]
                self.narupa_client.set_shared_value('interaction mode', self.current_interaction_mode)

            # Currently in Section 2 of the game.
            elif '2' in task:
                self.narupa_client.set_shared_value('current section', 1)
                self.current_interaction_mode = self.order_of_interaction_modes[1]
                self.narupa_client.set_shared_value('interaction mode', self.current_interaction_mode)

            else:
                raise Exception('The order of tasks must contain 1 or 2.')

            if 'P' in task:
                self.current_task_type = 'nanotube'

            elif 'A' in task:
                self.current_task_type = 'knot-tying'

            elif 'B' in task:
                self.current_task_type = 'trials'

            else:
                raise Exception('The order of tasks must contain P, A, or B.')

            # Start current task.
            self.initialise_task()

        # Finished all tasks, end the game.
        self.finish_game()

    def initialise_task(self):
        """ Handles the initialisation of each task. """

        if not self.current_task_type:
            raise Exception("No task specified.")

        if not self.current_task_index:
            # First task.
            self.current_task_index = 0
        else:
            # Increment current task index.
            self.current_task_index += 1

        # Write to shared state about current task.
        self.narupa_client.set_shared_value('task', self.current_task_type)
        self.narupa_client.set_shared_value('task status', 'in progress')
        self.current_task_status = 'in progress'

        if self.current_task_type == 'nanotube':
            self.narupa_client.set_shared_value('simulation index', self.nanotube_index)
            self.run_nanotube_task()

        elif self.current_task_type == 'knot-tying':
            self.narupa_client.set_shared_value('simulation index', self.alanine_index)
            self.run_knot_tying_task()

        elif self.current_task_type == 'trials':
            self.run_psychophysical_trials()

        else:
            raise Exception('The task type must one of the following: nanotube, knot-tying, or trials.')

    def finish_task(self):
        """Handles the finishing of each task."""

        # Update information in shared state.
        self.narupa_client.set_shared_value('task status', 'finished')
        self.current_task_status = 'finished'

        # Reset the required variables.
        if self.current_task_type == 'nanotube':
            self.was_methane_in_nanotube = False
            self.is_methane_in_nanotube = False
            self.methane_end_of_entry = None
        elif self.current_task_type == 'knot-tying':
            self.knot_pull_client = None

        # Wipe current task type.
        self.current_task_type = None

    def run_knot_tying_task(self):
        """ Starts the knot-tying task, where the user attempts to tie a trefoil knot in the 17-alanine polypeptide."""

        # Load and start the simulation.
        self.narupa_client.run_command("playback/load", index=self.alanine_index)
        self.narupa_client.run_command("playback/play")

        # Load the module for detecting knots.
        self.knot_pull_client = RefNarupaknotpullclient(atomids=self.narupa_client.current_frame.particle_names,
                                                        resids=self.narupa_client.current_frame.residue_ids,
                                                        atom_positions=self.narupa_client.current_frame.particle_positions)

        # Keeping checking if chain is knotted.
        while True:

            self.knot_pull_client.check_if_chain_is_knotted(
                atom_positions=self.narupa_client.current_frame.particle_positions)

            if self.knot_pull_client.is_currently_knotted:
                self.narupa_client.set_shared_value('task status', 'completed')
                time.sleep(3)
                break

            time.sleep(1 / 30)

        self.finish_task()

    def run_nanotube_task(self):
        """ Starts the nanotube + methane task. The task ends when the methane has been threaded through the
        nanotube."""

        # Load and start the simulation.
        self.narupa_client.run_command("playback/load", index=self.nanotube_index)
        self.narupa_client.run_command("playback/play")

        # Wait until task is completed.
        self.wait_for_methane_to_be_threaded()
        self.finish_task()

    def wait_for_methane_to_be_threaded(self):
        """ Continually checks if the methane has been threaded through the nanotube."""

        # TODO: Ensure that the user interacts with the methane as a residue for this task. To be done by the VR client.
        self.narupa_client.clear_selections()
        nanotube_selection = self.narupa_client.create_selection("CNT", list(range(0, 60)))
        nanotube_selection.remove()
        with nanotube_selection.modify() as selection:
            selection.renderer = \
                {'render': 'ball and stick',
                 'color': {'type': 'particle index', 'gradient': ['white', 'SlateGrey', [0.1, 0.5, 0.3]]}
                 }

        # TODO: This does not currently check whether the methane is threaded through the correct (specified) end of
        #  the nanotube, it just checks that the methane has been threaded fully. We may need to update this
        #  functionality if we are going to instruct the user on which end to thread it through.
        while True:

            # Get current positions of the methane and nanotube.
            nanotube_carbon_positions = np.array(self.narupa_client.latest_frame.particle_positions[0:59])
            methane_carbon_position = np.array(self.narupa_client.latest_frame.particle_positions[60])

            # Check if methane is in the nanotube.
            self.was_methane_in_nanotube = self.is_methane_in_nanotube
            self.is_methane_in_nanotube = ref_check_if_point_is_inside_shape(point=methane_carbon_position,
                                                                             shape=nanotube_carbon_positions)

            # Logic for detecting whether the methane has been threaded.
            if not self.was_methane_in_nanotube and self.is_methane_in_nanotube:

                # Methane has entered the nanotube.
                self.methane_end_of_entry = ref_get_closest_end(entry_pos=methane_carbon_position,
                                                                first_pos=nanotube_carbon_positions[0],
                                                                last_pos=nanotube_carbon_positions[-1])

            if self.was_methane_in_nanotube and not self.is_methane_in_nanotube:
                # Methane has exited the nanotube.
                methane_end_of_exit = ref_get_closest_end(entry_pos=methane_carbon_position,
                                                          first_pos=nanotube_carbon_positions[0],
                                                          last_pos=nanotube_carbon_positions[-1])

                if self.methane_end_of_entry != methane_end_of_exit:
                    # Methane has been threaded!
                    time.sleep(3)
                    break

                self.methane_end_of_entry = None

            time.sleep(1 / 30)

    def run_psychophysical_trials(self):
        """ Starts the psychophysical trials task. At the moment, each simulation runs for 10 seconds."""

        trials = ref_randomise_order_of_trials(self.buckyball_indices * self.num_trial_repeats)

        for sim in trials:
            self.narupa_client.set_shared_value('simulation index', sim)
            self.narupa_client.run_command("playback/load", index=trials[sim])
            self.narupa_client.run_command("playback/play")
            time.sleep(10)

        self.finish_task()

    def finish_game(self):
        # TODO: add anything here that needs to be done at the end of the game. E.g., sending last bit of data to the
        #  server.
        pass


if __name__ == '__main__':
    print("Running puppeteering client script\n")
    puppeteering_client = RefPuppeteeringClient()

    puppeteering_client.start_game()

    # # When an avatar connects, start the knot detection task
    # print("Waiting for avatar to connect.")
    # while True:
    #
    #     # check state dictionary for avatar
    #     is_avatar_connected = [value for key, value in
    #                            puppeteering_client.narupa_client.latest_multiplayer_values.items()
    #                            if 'avatar' in key.lower()]
    #
    #     if is_avatar_connected:
    #         print("Avatar connected. Starting task.")
    #         break
    #
    #     time.sleep(1)

    print("Closing the narupa client.")
    puppeteering_client.narupa_client.close()
