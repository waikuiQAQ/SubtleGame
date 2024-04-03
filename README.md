# SubtleGame

## Cloning the repo

1. Open "Anaconda Powershell Prompt" (if you already have Anaconda installed), or else open "Command Prompt".
2. Install [git](https://github.com/git-guides/install-git).
3. Navigate to the local directory where you want the SubtleGame git repo.
4. Clone the repo by typing: `git clone paste-repo-URL-here`.

## Python client

The game is handled by a Python client that is referred to as the 'puppeteering client' and can be found here: `./Client/puppeteering-client.py`.
1. Install Anaconda.
2. Open "Anaconda Powershell Prompt" and type the following commands.
    - `conda create -n subtle-game "python>3.9"` to create a Conda environment called `subtle-game`.
    - `conda activate subtle-game` to activate the environment you have just created.
3. Install the following packages in this environment by clicking on the following URLs and following the up-to-date installation instructions.
    - [Numpy](https://anaconda.org/anaconda/numpy)
    - [Random-Username](https://pypi.org/project/random-username/)
    - [Nanover Protocol](https://github.com/IRL2/nanover-protocol), by typing `conda install -c irl -c omnia -c conda-forge nanover-server` into your terminal.
    - [Knot-Pull](https://github.com/dzarmola/knot_pull)
4. Open the `SubtleGame` directory in your favourite Python IDE. Select the `subtle-game` conda environment as your python interpreter and set the `SubtleGame` directory to be the root. Note that if you are running the puppeteering-client script from the terminal, ensure that you have activated the subtle-game environment by typing `conda activate subtle-game`.

## VR client

1. Install and open Unity Hub.
2. Click the `Add` button and select the `./Client/vr-client` directory.
3. If not already installed, you should get a prompt to install the required version of Unity (2022.3.8f1). Install this along with the Android Build Support with OpenJDK and Android SDK & NDK Tools.
4. Open the game using this version of Unity and open the `Main` scene, which is found in the `./Assets/Scenes` directory.

### Oculus PC App Settings

The game can be played on a Quest 2 or 3 headset using Quest Link or AirLink.
1. Install the Oculus PC app for Meta Quest Link.
2. Open the app and ensure that OpenXR Runtime is active by going to `Settings` -> `General` and selecting `Set Oculus as active` for the OpenXR Runtime option. If this option is not selected then you will receive the warning `unable to start Oculus XR plugin` in the Unity console when you click play.
3. Enable passthrough by going to `Settings` -> `Beta`. Toggle the button to enable `Developer runtime features` and then toggle the option for `Pass-through over oculus link`. This allows the game to use passthrough, where you can see your physical surroundings through the cameras on the VR headset. 

### Oculus settings inside the headset

Hand tracking must be enabled on your VR headset to play the game. To do this:
1. Navigate to Settings from inside your headset and select `Movement tracking`. 
2. Toggle on the `Hand and body tracking` option and click `Enable`.

## Running a game

1. Run a server by navigating to `./Client/rust-server-2023-10-19` and clicking `nanover-gui.exe`. Open the Network tab and change the Server name to `SubtleGame`.

You will need to load a minimum of three simulations:
- The nanotube + methane: `nanotube_langevin.xml`
- The 17-alanine polypeptide: `17-ala.xml`
- A buckyball simulation: e.g., `buckyballs_angle_A_0.5.xml`
- The sandbox simulation: `sandbox_2_C10_alkanes.xml`

You can load more buckyball simulations if you wish. 

2. To load the simulations, select `File input` and click on the `+` and `-` symbols to add and remove simulations. Click `Select files` and choose one of the files located in the `\Inputs` directory. Repeat this until you have all the required simulations, then click `Run the selected file!`.
4. Run the Python script `./Client/puppeteering-client.py` from inside your `subtle-game` conda environment (either using the terminal or your Python IDE, as detailed above). A randomly-generated username will appear on the terminal. Type `y` and press `Enter` on your keyboard to accept this username and continue, or alternatively press `Enter` to generate a new username.
5. Open `Oculus Link` or `Air Link` from inside your Oculus headset.
6. Open Unity and click play to start the game.

IMPORTANT NOTE: both the VR client and puppeteering client are hardcoded to connect to a locally-running server called "SubtleGame". This will cause issues if you are on the same network as another person who is also running the game. If you want to change the server name, you need to change this in the VR client (`./Client/vr-client/Assets/NarupaIMD/Subtle Game/SubtleGameManager.cs`) and the puppeteering client (`./Client/puppeteering_client.py"`), and then type this server name into the server before you start.

