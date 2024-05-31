﻿using Nanover.Visualisation;
using UnityEngine;

namespace NanoverIMD.Subtle_Game.UI.Simulation
{
    public class BackFace : MonoBehaviour
    {
        [SerializeField]
        private SynchronisedFrameSource frameSource;

        /// <summary>
        /// Sets the position of this game object to the center of the back of the simulation box.
        /// </summary>
        public void Update()
        {
            // Update position of current game object
            if (frameSource.CurrentFrame is not { BoxVectors: { } box }) return;
            transform.localPosition = new Vector3(
                box.axesMagnitudes.x * 0.5f,
                box.axesMagnitudes.x * 0.25f,
                box.axesMagnitudes.x * 0.0f);
            transform.localRotation = Quaternion.LookRotation(Vector3.back);
        }
    }
}