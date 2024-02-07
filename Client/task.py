from narupa.app import NarupaImdClient
from additional_functions import write_to_shared_state
import time
from standardised_values import *


class Task:
    task_type = None
    timestamp_start = None
    timestamp_end = None
    task_completion_time = None

    def __init__(self, client: NarupaImdClient, simulations: list, sim_counter: int):

        self.client = client
        self.simulations = simulations
        self.simulation_counter = sim_counter

        for sim in self.simulations[0]:
            self.sim_index = self.simulations[0][sim]
            self.sim_name = sim

    def run_task(self):

        self._prepare_task()

        self._wait_for_vr_client_to_start_task()

        self._run_task_logic()

        self._finish_task()

    def _prepare_task(self):

        # Load simulation
        self._request_load_simulation()

        print("Waiting for simulation to load")
        self._wait_for_simulation_to_load()

        print("Simulation loaded")

        # Update visualisation
        self._update_visualisations()

        # Pause simulation
        self.client.run_command("playback/pause")

        # Update shared state
        write_to_shared_state(client=self.client, key=key_simulation_name, value=self.sim_name)
        write_to_shared_state(client=self.client, key=key_simulation_server_index, value=self.sim_index)
        write_to_shared_state(client=self.client, key=key_current_task, value=self.task_type)
        write_to_shared_state(client=self.client, key=key_task_status, value=ready)

        print("Task prepared")

    def _wait_for_simulation_to_load(self):
        """ Waits for the simulation to be loaded onto the server by checking if the simulation counter has
        incremented."""
        while True:

            try:
                current_val = self.client._current_frame.values["system.simulation.counter"]
                if current_val == self.simulation_counter + 1:
                    break

            except KeyError:
                time.sleep(1 / 30)

        self.simulation_counter += 1

    def _request_load_simulation(self):
        """ Loads the simulation. """
        self.client.run_command("playback/load", index=self.sim_index)

    def _wait_for_vr_client_to_start_task(self):

        print('Waiting for player to start task')
        while True:

            try:
                # check whether the value matches the desired value for the specified key
                current_val = self.client.latest_multiplayer_values[key_player_task_status]

                if current_val == player_in_progress or current_val == player_practice_in_progress:
                    break

            except KeyError:
                # If the desired key-value pair is not in shared state yet, wait a bit before trying again
                time.sleep(1 / 30)

    def _update_visualisations(self):
        """ Container for changing the task-specific visualisation the simulation. """
        pass

    def _run_task_logic(self):
        """Container for the logic specific to each task."""

        print('Starting task')

        # Play simulation
        self.client.run_play()

        # Check that frames are being received
        while True:
            try:
                _ = self.client.latest_frame.particle_positions
                break
            except KeyError:
                print("No particle positions found, waiting for 1/30 seconds before trying again.")
                time.sleep(1 / 30)

        # Update shared state
        write_to_shared_state(client=self.client, key=key_task_status, value=in_progress)

    def _check_if_sim_has_blown_up(self):
        """ Resets the simulation if the kinetic energy goes above a threshold value. """
        try:
            if self.client.latest_frame.kinetic_energy > 10e10:
                self.client.run_reset()
        except KeyError:
            pass

    def _finish_task(self):
        """Handles the finishing of the task."""

        # Update task status and completion time in the shared state
        write_to_shared_state(client=self.client, key=key_task_status, value=finished)

        if self.timestamp_start and self.timestamp_end:
            self.task_completion_time = self.timestamp_end - self.timestamp_start
            write_to_shared_state(client=self.client,
                                  key=key_task_completion_time,
                                  value=str(self.task_completion_time))

        # Wait for player to register that the task has finished
        print('Waiting for player to confirm end of task')
        while True:

            try:
                # check whether the value matches the desired value for the specified key
                current_val = self.client.latest_multiplayer_values[key_player_task_status]

                if current_val == player_finished:
                    break

            except KeyError:
                # If the desired key-value pair is not in shared state yet, wait a bit before trying again
                time.sleep(1 / 30)
