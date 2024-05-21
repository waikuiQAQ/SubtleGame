# ---------------- #
# GENERAL
# ---------------- #
# Server
SERVER_NAME = 'SubtleGame'
# Task
TASK_SANDBOX = 'sandbox'
TASK_NANOTUBE = 'nanotube'
TASK_KNOT_TYING = 'knot-tying'
TASK_TRIALS = 'trials'
# Simulation
SIM_NAME_SANDBOX = 'sandbox'
SIM_NAME_NANOTUBE = 'nanotube'
SIM_NAME_KNOT_TYING = '17-ala'
SIM_NAME_TRIALS = 'buckyball'
# Frequency
STANDARD_FREQUENCY = 30
STANDARD_RATE = 1 / STANDARD_FREQUENCY
# Colours
IRL_ORANGE = [1, 0.39, 0.016]
IRL_BLUE = [0, 0, 0.8]

# ---------------- #
# KEYS
# ---------------- #
KEY_USERNAME = 'participant-username'
KEY_MODALITY = 'modality'
KEY_GAME_STATUS = 'game-status'
KEY_ORDER_OF_TASKS = 'order-of-tasks'
KEY_SIM_COUNTER = 'system-simulation-counter'
KEY_CURRENT_TASK = 'current-task'
KEY_TASK_STATUS = 'task-status'
KEY_TRIALS_SIMS = 'trials-simulations'
KEY_NUMBER_OF_TRIALS = 'number-of-trials'
KEY_NUMBER_OF_TRIAL_REPEATS = 'number-of-trial-repeats'
KEY_TRIALS_TIMER = 'trials-timer'
KEY_TRIALS_ANSWER = 'trials-answer'
KEY_TASK_COMPLETION_TIME = 'task-completion-time'
KEY_SIMULATION_NAME = 'simulation-name'
KEY_SIMULATION_SERVER_INDEX = 'simulation-server-index'

# ---------------- #
# VALUES
# ---------------- #
# Status
READY = 'ready'
WAITING = 'waiting'
STARTED = 'started'
IN_PROGRESS = 'in-progress'
FINISHED = 'finished'
AMBIVALENT = 'Ambivalent'
TRUE = 'True'
FALSE = 'False'
# Interaction modality
MODALITY_HANDS = 'hands'
MODALITY_CONTROLLERS = 'controllers'

# ---------------- #
# PLAYER
# ---------------- #
KEY_PLAYER_CONNECTED = 'Player.Connected'
KEY_PLAYER_TASK_TYPE = 'Player.TaskType'
KEY_PLAYER_TASK_STATUS = 'Player.TaskStatus'
KEY_PLAYER_TRIAL_NUMBER = 'Player.TrialNumber'
KEY_PLAYER_TRIAL_ANSWER = 'Player.TrialAnswer'
PLAYER_INTRO = 'Intro'
PLAYER_SANDBOX = 'Sandbox'
PLAYER_NANOTUBE = 'Nanotube'
PLAYER_KNOT_TYING = 'KnotTying'
PLAYER_TRIALS = 'Trials'
PLAYER_IN_PROGRESS = 'InProgress'
PLAYER_FINISHED = 'Finished'

# ---------------- #
# SHARED STATE
# ---------------- #
SHARED_STATE_KEYS_AND_VALS = {
    KEY_MODALITY: [MODALITY_HANDS, MODALITY_CONTROLLERS],
    KEY_GAME_STATUS: [WAITING, IN_PROGRESS, FINISHED],
    KEY_ORDER_OF_TASKS: [TASK_NANOTUBE, TASK_KNOT_TYING, TASK_TRIALS],
    KEY_CURRENT_TASK: [TASK_SANDBOX, TASK_NANOTUBE, TASK_KNOT_TYING, TASK_TRIALS],
    KEY_TASK_STATUS: [READY, IN_PROGRESS, FINISHED],
    KEY_TRIALS_TIMER: [STARTED, FINISHED],
    KEY_TRIALS_ANSWER: [AMBIVALENT, TRUE, FALSE]
}

KEYS_WITH_UNRESTRICTED_VALS = [KEY_TASK_COMPLETION_TIME, KEY_SIMULATION_NAME, KEY_SIMULATION_SERVER_INDEX,
                               KEY_TRIALS_SIMS, KEY_NUMBER_OF_TRIALS, KEY_NUMBER_OF_TRIAL_REPEATS, KEY_USERNAME,
                               KEY_SIM_COUNTER]
