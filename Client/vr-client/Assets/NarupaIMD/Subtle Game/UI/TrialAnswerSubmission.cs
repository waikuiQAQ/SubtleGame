﻿using System;
using System.Collections;
using Narupa.Visualisation.Components.Input;
using UnityEngine;

namespace NarupaIMD.Subtle_Game.UI
{
    public class TrialAnswerSubmission : MonoBehaviour
    {
        [SerializeField] private CentreOfGeometry cogA;
        [SerializeField] private Transform rightThumbTip;
        
        private GameObject _molecule;
        private ColorInput _moleculeColor;
        
        private readonly Color _originalColor = new(0f, 0f, 1.0f, 1.0f);
        private readonly Color _endColor = new(0f, 1f, 0f, 1.0f);
        private Color _targetColor;
        
        private const float ColorChangeDuration = 2.0f;
        
        private bool _isSelected;
        private bool _wasInsideLastFrame;
        
        /// <summary>
        /// Runs logic for waiting for an answer from the player to the psychophysics trials task.
        /// </summary>
        public void RequestAnswerFromPlayer(string moleculeName = "BUC_A")
        {
            GetMoleculeObject(moleculeName);
            cogA.CalculateCentreOfGeometry();
            
            for (int i = 0; i < _molecule.transform.childCount; i++)
            {
                Transform childTransform = _molecule.transform.GetChild(i);
                _moleculeColor = childTransform.GetComponent<ColorInput>();
            }
            
            StartCoroutine(WaitForAnswer());
        }
        
        /// <summary>
        /// Gets the molecule game object.
        /// </summary>
        private void GetMoleculeObject(string moleculeName)
        {
            _molecule = GameObject.Find(moleculeName);
            if (_molecule == null)
            {
                Debug.LogWarning("Molecule game object was not found, cannot change it's colour."); 
            }
        }
        
        /// <summary>
        /// Waits for the player to select their answer by placing their hand inside the molecule of choice. This
        /// function checks if the players hand is inside the molecule. If yes, the molecule will start changing colour.
        /// If the hand is inside the molecule for the desired lenght of time, that molecule is the submitted as the
        /// player's answer.
        /// </summary>
        private IEnumerator WaitForAnswer()
        {
            _targetColor = _originalColor;
            
            while (true)
            {
                // Check if the hand is inside the molecule
                bool isInside = cogA.IsPointInsideShape(rightThumbTip.position);

                // Check if hand has changed position
                if (isInside != _wasInsideLastFrame)
                {
                    // Reset the color change timer
                    float timer = 0f;

                    // Update the target color based on the current state
                    _targetColor = isInside ? _endColor : _originalColor;
                    _moleculeColor.Node.Input.Value = _targetColor;

                    // Interpolate the color over time
                    while (timer <= ColorChangeDuration)
                    {
                        // Lerp the color of the molecule
                        _moleculeColor.Node.Input.Value = Color.Lerp(_originalColor, _targetColor, timer / ColorChangeDuration);

                        // Increment the timer
                        timer += Time.deltaTime;
                        
                        // Wait for the next frame
                        yield return null; 
                        
                        // Break the colour-lerping loop if the hand has changed position
                        if (cogA.IsPointInsideShape(rightThumbTip.position) != isInside)
                        {
                            break; 
                        }
                        
                        // Participant has selected their answer if the time duration has been completed
                        if (Math.Abs(timer - ColorChangeDuration) < 0.01f && isInside)
                        {
                            _isSelected = true;
                        }
                    }

                    // Update the boolean for the next frame
                    _wasInsideLastFrame = isInside;
                }

                if (_isSelected)
                {
                    Debug.Log("Player has answered");
                    break;
                }
                
                // Wait for the next frame
                yield return null;
            }
        }
    }
}