from task import Task
from nanover.app import NanoverImdClient
from datetime import datetime
from standardised_values import *
from additional_functions import write_to_shared_state,remove_puppeteer_key_from_shared_state
import time
import numpy as np
from datetime import datetime

ATOM_MASS_DICT = {
    1: 1.008,    # H
    6: 12.01,    # C
    7: 14.01,    # N
    8: 16.00,    # O
}
UNBINGD_DISTANCE = 1.8
class UnbindGluhutTask(Task):
    task_type = TASK_UNBINDGLUHUT

    def __init__(self, client: NanoverImdClient, simulations: list, simulation_counter: int, userName:str):

        super().__init__(client, simulations, sim_counter=simulation_counter)
        self.userName = userName
        self.number_of_trial = 3
        self.subtask_count = 0
        self.subtask_start_time = None
    def run_task(self):
        #self._run_task_onebyone()
        self._run_task_three_times()

        self._finish_task()  # End trials
        remove_puppeteer_key_from_shared_state(self.client, KEY_BIND_STATUS)
    def _run_task_three_times(self):
        for trial_num in range(self.number_of_trial):
            
            #self.client.run_play()  
            self._prepare_trial (name="gluctose", server_index=0) #temp
            self.client.run_play()
            
            #self._start_subtask()
            if trial_num == 0:
                write_to_shared_state(self.client, KEY_TASK_STATUS, IN_PROGRESS)

            self._wait_for_player_to_complete()
            #self._finish_subtask()
        print("now user finished gluctose, prepare fructose")
        for trial_num in range(self.number_of_trial):
            self._prepare_trial (name="fructose", server_index=1) #temp
            self.client.run_play()
            #self._start_subtask()
            self._wait_for_player_to_complete()
            #self._finish_subtask()

        print("now user finished fructose")    

    def _run_task_onebyone(self):

        for trial_num in range(self.number_of_trial):
            
            #self.client.run_play()  
            self._prepare_trial (name="gluctose", server_index=0) #temp
            self.client.run_play()
            
            #self._start_subtask()
            if trial_num == 0:
                write_to_shared_state(self.client, KEY_TASK_STATUS, IN_PROGRESS)

            self._wait_for_player_to_complete()
            #self._finish_subtask()
            print("now user finished gluctose, prepare fructose")
            self._prepare_trial (name="fructose", server_index=1) #temp
            self.client.run_play()
            #self._start_subtask()
            self._wait_for_player_to_complete()
            #self._finish_subtask()
            print("now user finished fructose, prepare gluctose again")

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

        water_selection = self.client.create_selection("WAT", list(range(183, 12084)))
        water_selection.remove()
        with water_selection.modify() as selection:
            selection.hide = True
            #selection.interaction_method = "none"

    def check_if_unbinded(self, distance):
        if distance > UNBINGD_DISTANCE:
            return True
        return False
    def _start_subtask(self):
        #update the current task number
        subtask_id = f"{self.userName}{self.subtask_count}"
        self.current_subtask_id = subtask_id  
        self.subtask_count += 1
        #open the file to record the data

        #record the time of task start
        self.subtask_start_time = datetime.now()
        print(f"Subtask {subtask_id} started at {self.subtask_start_time}.")
        return
    def _finish_subtask(self):
        #close all the records
        #record the time of now - task start
        end_time = datetime.now()
        duration = (end_time - self.subtask_start_time).total_seconds()
        print(f"Subtask {self.current_subtask_id} finished. Duration: {duration} seconds.")
        #wirte the time to the file
        return
    
def calculateCentreOfMass(particle_elements, particle_positions):
        masses = np.array([ATOM_MASS_DICT.get(atomic_number, 0) for atomic_number in particle_elements])
        total_mass = masses.sum()
        if total_mass == 0:
            raise ValueError("Total mass is zero; check particle_elements.")
        centre_of_mass = (masses[:, np.newaxis] * np.array(particle_positions)).sum(axis=0) / total_mass
        return centre_of_mass
    
def GetCentreOfMassDistance(pos1, pos2):

    distance = np.linalg.norm(pos1 - pos2)
    return distance
# Define a function to start recording
def start_dcdrecording(simulation, file_name):
    dcd_reporter = app.DCDReporter(f"{file_name}.dcd", 100)
    simulation.reporters.append(dcd_reporter)
    print(f"Started recording for {file_name}.")
    return dcd_reporter

# Define a function to stop recording
def stop_dcdrecording(simulation, dcd_reporter):
    simulation.reporters.remove(dcd_reporter)
    print("Recording stopped and reporters removed.")