﻿using NanoverImd.Interaction;
using UnityEngine;

namespace NanoverIMD.Subtle_Game.Interaction
{
    /// <summary>
    /// Handles the rendering of the interaction lines of all known interactions.
    /// </summary>
    public class InteractionRendererManager : RendererManager<InteractionRenderer>
    {
        /// <summary>
        /// Update the values for the renderer associated with this interaction.
        /// </summary>
        protected override void ConfigureRenderer(ParticleInteraction interaction, InteractionRenderer rendererInstance, Vector3 particlePositionWorld)
            {
                rendererInstance.scale = interaction.Scale;
                rendererInstance.EndPosition = transform.TransformPoint(interaction.Position);
                rendererInstance.StartPosition = particlePositionWorld;
            }
    }
}