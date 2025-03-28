﻿using System.Collections;
using NanoverImd.Subtle_Game;
using NanoverImd.Subtle_Game.Canvas;
using NanoverImd.Subtle_Game.Data_Collection;
using NanoverIMD.Subtle_Game.Data_Collection;
using NanoverImd.Subtle_Game.Interaction;
using NanoverImd.Subtle_Game.UI.Simulation;
using UnityEngine;
using UnityEngine.Serialization;

namespace NanoverIMD.Subtle_Game.UI.Canvas
{
    public class TaskInstructionsManager : MonoBehaviour
    {
        /// <summary>
        /// Game object for the trials timer
        /// </summary>
        [SerializeField] private GameObject timer;
        
        /// <summary>
        /// Game object with the instructions on how interact with molecules using hands.
        /// </summary>
        [SerializeField] private GameObject inputHandInstructions;
        
        /// <summary>
        /// Game object with the instructions on how interact with molecules using controllers.
        /// </summary>
        [SerializeField] private GameObject inputControllerInstructions;

        /// <summary>
        /// Game object with the instructions on how interact with molecules using controllers.
        /// </summary>
        [SerializeField] private GameObject inputBothInputsInstructions;
        
        /// <summary>
        /// Game object with the instructions on knot tie instructions.
        /// </summary>
        [SerializeField] private GameObject taskKnotInstructions;

        /// <summary>
        /// Game object with the instructions on the Nano tube task.
        /// </summary>
        [SerializeField] private GameObject taskNanotubeInstructions;

        /// <summary>
        /// Game object with the instructions on what to do in sandbox mode.
        /// </summary>
        [SerializeField] private GameObject taskSandboxInstructions;

        /// <summary>
        /// Game object with the instructions on what to do in sandbox mode.
        /// </summary>
        [SerializeField] private GameObject taskTrialsInstructions;

        /// <summary>
        /// Game object with the instructions on how to exit the simulation (sandbox mode).
        /// </summary>
        [SerializeField] private GameObject exitInstructions;
        /// <summary>
        /// Game object with the instructions on BindGluhut.
        /// </summary>
        [SerializeField] private GameObject taskBindGluhutInstructions;
        /// <summary>
        /// Game object with the instructions on unbindGluhut.
        /// </summary>
        [SerializeField] private GameObject taskUnbindGluhutInstructions;
        /// <summary>
        /// The user interaction manager.
        /// </summary>
        [SerializeField] private UserInteractionManager userInteractionManager;
        
        /// <summary>
        /// The game object representing the center of the XY plane of the simulation box.
        /// </summary>
        [SerializeField] private CenterRightFace centerRightFace;
        
        /// <summary>
        /// The Trial Icon Manager.
        /// </summary>
        [SerializeField] private TrialManager trialProgressManager;

        // <summary>
        // The game object group to set the visibility of the progress
        // <summary>
        [SerializeField] private GameObject trialsProgressGroup;

        /// <summary>
        /// The Subtle Game Manager.
        /// </summary>
        private SubtleGameManager _subtleGameManager;
        
        [SerializeField] private TrialAnswerSubmission trialAnswerSubmission;

        // <summary>
        // Panel game object containing all of the instructions elements
        // </summary>
        private GameObject _panel;

        [SerializeField] private GameObject selectingAnswerForTrialsInstructions;

        /// <summary>
        /// Gets the Subtle Game Manager and hides the in-task instructions canvas.
        /// </summary>
        private void Start()
        {
            _subtleGameManager = FindObjectOfType<SubtleGameManager>();

            _panel = gameObject.transform.GetChild(0).gameObject;

            _panel.SetActive(false);
        }

        private void OnEnable()
        {
            trialAnswerSubmission.PlayerIsSelectingAnswer += HandlePlayerIsSelectingAnswer;
        }
        private void OnDisable()
        {
            trialAnswerSubmission.PlayerIsSelectingAnswer -= HandlePlayerIsSelectingAnswer;
        }

        /// <summary>
        /// Updates the in-task instructions based on the current interaction modality set in the Pinch Grab script.
        /// </summary>
        private void LateUpdate()
        {
            if (_subtleGameManager is null) return;

            // To overcome race conditions, we position and setup the input instructions constantly
            PlacePanelOnRightFaceOfSimBox();
            SetupInputInstructions();

            // Check the following: the sim is showing, the panel is not already active, and the task has changed
            if (_subtleGameManager.ShowSimulation && _panel.activeSelf==false)
            {
                // Position panel
                PlacePanelOnRightFaceOfSimBox();
                SetupLayout();
                
                // It takes a few frames for the box to be correctly positioned, so enable panel with slight delay
                StartCoroutine(DelayedSetActive(_panel, true, 0.1f));
            }

            // Do nothing if the simulation is still showing or the panel is not active
            if (_subtleGameManager.ShowSimulation || !_panel.activeSelf) return;

            // Hide instructions panel
            _panel.SetActive(false);
        }
        
        /// <summary>
        /// Enable a game object with a slight delay.
        /// </summary>
        private IEnumerator DelayedSetActive(GameObject obj, bool value, float seconds)
        {
            yield return new WaitForSeconds(seconds);
            obj.SetActive(value);
        }
        
        /// <summary>
        /// Call the functions to position the panel and activate the required elements.
        /// </summary>
        private void SetupLayout()
        {
            SetupTaskElements();
            SetupInputInstructions();
        }

        // <summary>
        //  Activate the required elements for the given task.
        // </summary>
        private void SetupTaskElements()
        {
            // hide all the objects. start with an empty canvas
            foreach (Transform child in _panel.transform)
            {
                child.gameObject.SetActive(false);
            }

            // activate the instruction objects required for each task type
            switch (_subtleGameManager.CurrentTaskType)
            {
                case SubtleGameManager.TaskTypeVal.KnotTying:
                    taskKnotInstructions.SetActive(true);
                    break;

                case SubtleGameManager.TaskTypeVal.Nanotube:
                    taskNanotubeInstructions.SetActive(true);
                    break;

                case SubtleGameManager.TaskTypeVal.Sandbox:
                    taskSandboxInstructions.SetActive(true);
                    exitInstructions.SetActive(true);
                    break;
                case SubtleGameManager.TaskTypeVal.BindGluhut:
                    taskBindGluhutInstructions.SetActive(true);
                    break;
                case SubtleGameManager.TaskTypeVal.UnbindGluhut:
                    taskUnbindGluhutInstructions.SetActive (true);
                    break;  

                default:
                    if (!TaskLists.TrialsTasks.Contains(_subtleGameManager.CurrentTaskType)) return;
                    taskTrialsInstructions.SetActive(true);
                    timer.SetActive(true);
                    trialProgressManager.gameObject.SetActive(true);
                    trialsProgressGroup.SetActive(true);
                    break;
            }
        }

        // <summary>
        // Activate the corresponding interaction instructions for the given task and interaction mode.
        // </summary>
        private void SetupInputInstructions()
        {
           if (_subtleGameManager.CurrentTaskType == SubtleGameManager.TaskTypeVal.Sandbox)
           {
                inputBothInputsInstructions.SetActive(true);
           }
           else
           {
                inputHandInstructions.SetActive( !userInteractionManager.UseControllers );
                inputControllerInstructions.SetActive( userInteractionManager.UseControllers );
           }
        }
        
        /// <summary>
        /// Place the in-task instructions at right face of the simulation box.
        /// </summary>
        private void PlacePanelOnRightFaceOfSimBox()
        {
            gameObject.transform.position = centerRightFace.transform.position;
            gameObject.transform.rotation = centerRightFace.transform.rotation;
        }

        private void HandlePlayerIsSelectingAnswer(bool playerIsSelectingAnswer)
        {
            selectingAnswerForTrialsInstructions.SetActive(playerIsSelectingAnswer);
        }
    }
}