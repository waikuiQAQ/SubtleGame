from narupa.app import NarupaImdClient
from task_nanotube import NanotubeTask
from task_knot_tying import KnotTyingTask
from task_trials import Trial
from additional_functions import write_to_shared_state


class PuppeteeringClient:
    """ This class interfaces between the Nanover server, VR client and any required packages to control the game 
    logic for the Subtle Game."""

    def __init__(self):

        # Connect to a local Nanover server.
        self.narupa_client = NarupaImdClient.autoconnect(name="SubtleGame")
        self.narupa_client.subscribe_multiplayer()
        self.narupa_client.subscribe_to_frames()
        self.narupa_client.update_available_commands()

        # Declare variables.
        self.order_of_tasks = ['trials']
        self.order_of_modality = ['hands']
        self.current_modality = self.order_of_modality[0]

    def run_game(self):

        # initialise game
        self._initialise_game()
        print('Game initialised')

        # loop through the tasks
        for task in self.order_of_tasks:

            if task == 'nanotube':

                # Check that the nanotube simulation was loaded into the server
                if len(self.nanotube_index) == 0:
                    raise ValueError("No nanotube simulation found. Have you forgotten to load the simulation on the "
                                     "server? Does the loaded .xml contain the term 'nanotube?")

                current_task = NanotubeTask(self.narupa_client, simulation_index=self.nanotube_index[0])

            elif task == 'knot-tying':

                # Check that the nanotube simulation was loaded into the server
                if len(self.alanine_index) == 0:
                    raise ValueError("No 17-alanine simulation found. Have you forgotten to load the simulation on the "
                                     "server? Does the loaded .xml contain the term '17-ala'?")

                current_task = KnotTyingTask(self.narupa_client, simulation_index=self.alanine_index[0])

            elif task == 'trials':
                current_task = Trial(self.narupa_client, simulation_index=self.trials_index[0],
                                     simulation_name=self.trials_name[0])

            else:
                print("Current task not recognised, closing the puppeteering client.")
                break

            # Run the task
            print('\nRunning ' + task + ' task')
            current_task.run_task()
            print('Finished ' + task + ' task\n')

        # gracefully finish the game
        self._finish_game()
        print('Game finished')

    def _initialise_game(self):
        """ Writes the key-value pairs to the shared state that are required to begin the game. Gets simulation
        indexes from server."""

        # update the shared state
        write_to_shared_state(self.narupa_client, 'game-status', 'waiting')
        write_to_shared_state(self.narupa_client, 'modality', self.current_modality)
        write_to_shared_state(self.narupa_client, 'order-of-tasks', self.order_of_tasks)

        # Get simulation indices from server.
        simulations = self.narupa_client.run_command('playback/list')

        self.nanotube_index = [idx for idx, s in enumerate(simulations['simulations']) if 'nanotube' in s]

        self.alanine_index = [idx for idx, s in enumerate(simulations['simulations']) if '17-ala' in s]

        self.trials_index = [idx for idx, s in enumerate(simulations['simulations']) if 'buckyball' in s]
        self.trials_name = [s for idx, s in enumerate(simulations['simulations']) if 'buckyball' in s]

    def _finish_game(self):
        """ Update the shared state and close the client at the end of the game. """
        # finish game
        print("Closing the narupa client and ending game.")
        write_to_shared_state(self.narupa_client, 'game-status', 'finished')
        self.narupa_client.close()


if __name__ == '__main__':

    # Create puppeteering client
    puppeteering_client = PuppeteeringClient()

    # Start game
    print('Starting game\n')
    puppeteering_client.run_game()
