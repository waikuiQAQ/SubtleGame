from task import Task
from nanover.app import NanoverImdClient
from datetime import datetime
from standardised_values import *
from additional_functions import write_to_shared_state,remove_puppeteer_key_from_shared_state
import time
import numpy as np
from datetime import datetime
from nanover.omni.record import record_from_server
class BindGluhutTask(Task):
    task_type = TASK_BINDGLUHUT

    def __init__(self, client: NanoverImdClient, simulations: list, simulation_counter: int, userName:str):

        super().__init__(client, simulations, sim_counter=simulation_counter)
        self.userName = userName
        self.number_of_trial = 3
        self.subtask_count = 0
        self.subtask_start_time = None
        

    def run_task(self):

        for trial_num in range(self.number_of_trial):
            
            #self.client.run_play()  
            self._prepare_trial (name="gluctose", server_index=0)#temp
            traj_path = 'usertestTest_recording.traj'
            state_path = 'usertestTest_recording.state'
            record_from_server("38801",traj_path, state_path)
            self.client.run_play()
            #self._start_subtask()
            if trial_num == 0:
                write_to_shared_state(self.client, KEY_TASK_STATUS, IN_PROGRESS)

            self._wait_for_player_to_complete()
            #self._finish_subtask()
            print("now user finished gluctose binding")
            
        self._finish_task()  # End trials
        remove_puppeteer_key_from_shared_state(self.client, KEY_BIND_STATUS)
        
    def _prepare_trial(self, name, server_index):
        """ Set variables and prepare task for a new trial """
        self.sim_name = name
        self.sim_index = server_index
        
        self._prepare_task()
        print(f'Current trial: "{self.sim_name}"')
        self._wait_for_task_in_progress()


    def _wait_for_player_to_complete(self):
        """ Waits for the player to complete binding and updates shared state. """

        print(f"Waiting for player to complete...")
        self.client.remove_shared_value(KEY_BIND_STATUS)
        #self.client.set_shared_value(KEY_BIND_STATUS, BINDING)
        #print(self.client.latest_multiplayer_values[KEY_BIND_STATUS])
        try :
            print(self.client.latest_multiplayer_values[KEY_BIND_STATUS])
        except:
            print("No KEY_BIND_STATUS value")
        # Wait for player response
        self._wait_for_BIND_STATUS_key_values(KEY_BIND_STATUS, BINDEDFINISHED, UNBINDFINISHED)

        print("Player finish bind or unbing ")

    def _wait_for_BIND_STATUS_key_values(self, key, *values):
        while True:
            try:
                value = self.client.latest_multiplayer_values[key]
                if value in values:
                    break

            except KeyError:
                pass

            # If the desired key-value pair is not in shared state yet, wait a bit before trying again
            time.sleep(STANDARD_RATE)

    def _update_visualisations(self):
        print("Updating visualisations")
        my_first_selection = self.client.create_selection("REC", list(range(0, 159)))
        my_first_selection.remove()
        with my_first_selection.modify() as selection:
            selection.renderer = {
                    'color': 'cpk',
                    'scale': 0.08,
                    'render': 'liquorice'
                }

        my_second_selection = self.client.create_selection("0GB_ROH", list(range(159, 183)))
        my_second_selection.remove()

        with my_second_selection.modify() as selection:
            selection.interaction_method = "single" 
            selection.renderer = {
                'color': {
                    'type': 'cpk',
                    'scheme': 'nanover'
                },
                'scale': 0.04,
                'render': 'liquorice'
            } 
        water_selection = self.client.create_selection("WAT", list(range(183, 76126)))
        water_selection.remove()
        with water_selection.modify() as selection:
            selection.hide = True
            #selection.interaction_method = "none"