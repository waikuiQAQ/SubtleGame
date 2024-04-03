using Nanover.Core.Math;
using Nanover.Frame;
using Nanover.Frame.Event;
using Nanover.Visualisation;
using NarupaImd;
using NarupaIMD.Subtle_Game.UI.Simulation;
using UnityEngine;
using UnityEngine.Serialization;

namespace NarupaIMD.Subtle_Game.Visuals
{
    public class CenteringSimulationInFrontOfPlayer : MonoBehaviour
    {
        [SerializeField]
        private SynchronisedFrameSource frameSource;

        /// <summary>
        /// The NarupaIMD simulation.
        /// </summary>
        [SerializeField]
        private Transform simulation;

        /// <summary>
        /// The center eye anchor of the OVR Camera Rig.
        /// </summary>
        [SerializeField]
        private Transform centreEyeAnchor;

        /// <summary>
        /// The desired scale of the lengths of the simulation box.
        /// </summary>
        private float _simulationScale;
        
        /// <summary>
        /// The center of the xy plane of the simulation box.
        /// </summary>
        [SerializeField] private CenterXYPlane centerXYPlane;
        
        /// <summary>
        /// The center of the xy plane of the simulation box.
        /// </summary>
        [FormerlySerializedAs("centerXZPlane")] [SerializeField] private PointOfParticleEmission pointOfParticleEmission;

        /// <summary>
        /// Manager of the Subtle Game.
        /// </summary>
        public SubtleGameManager subtleGameManager;
        

        private void OnEnable()
        {
            frameSource.FrameChanged += OnFrameChanged;
        }

        private void OnDisable()
        {
            frameSource.FrameChanged += OnFrameChanged;
        }

        private void OnFrameChanged(IFrame frame, FrameChanges changes)
        {
            if (changes.HasChanged(StandardFrameProperties.BoxTransformation.Key))
            {
                var box = (frame as Frame)?.BoxVectors;
                if (box == null)
                {
                    nextXMagnitude = 0;
                }
                else
                {
                    nextXMagnitude = box.Value.axesMagnitudes.x;
                }
            }
        }

        private void Update()
        {
            CheckBoxChange();
        }

        private float prevXMagnitude;
        private float nextXMagnitude;

        private void CheckBoxChange()
        {
            if (Mathf.Abs(nextXMagnitude - prevXMagnitude) > 0.1f)
                UpdateSimulationBox();

            prevXMagnitude = nextXMagnitude;
        }

        /// <summary>
        /// Updates the scale and position of the simulation box relative to the player. NOTE: this code assumes that
        /// all sides of the box are equal in length.
        /// </summary>
        private void UpdateSimulationBox()
        {
            // Move simulation box
            SetSimulationScale();
            PutSimulationInFrontOfPlayer();
            centerXYPlane.PositionCenterOfXYPlane();
            pointOfParticleEmission.UpdatePosition();
            
            // Update scene in shared state
            var simBox = transform;
            var position = simBox.position;
            var rotation = simBox.rotation;
            var scale = simBox.lossyScale;
            subtleGameManager.simulation.Multiplayer.SimulationPose.UpdateValueWithLock(
                new Transformation(position, rotation, scale));
        }
        
        /// <summary>
        /// Sets the scale of the simulation. Default value is 1 (nanotube and trials tasks), with a smaller scale of
        /// 0.75 for the knot-tying task.
        /// </summary>
        private void SetSimulationScale()
        {
            // Get simulation scale value for each task
            _simulationScale = subtleGameManager.CurrentTaskType switch
            {
                SubtleGameManager.TaskTypeVal.Nanotube => 1f,
                SubtleGameManager.TaskTypeVal.KnotTying => 0.75f,
                SubtleGameManager.TaskTypeVal.Trials => 1f,
                _ => 1f
            };
            
            // Set the scale of the simulation game object
            simulation.transform.localScale = new Vector3(_simulationScale, _simulationScale,_simulationScale);
        }
        
        /// <summary>
        /// Puts the simulation in front of the player. The default is centering the headset on the xy plane of the
        /// simulation box, but these values are altered for the knot-tying task and the trials.
        /// </summary>
        private void PutSimulationInFrontOfPlayer()
        {
            // Set default values: centering the player on the xy plane of the simulation box facing the +z direction
            float xComponent = -nextXMagnitude * 0.5f;
            float yComponent = -nextXMagnitude * 0.5f;
            float zComponent = 0f;

            // Alter values for knot-tying and trials tasks
            switch (subtleGameManager.CurrentTaskType)
            {
                case SubtleGameManager.TaskTypeVal.KnotTying:
                    yComponent = -nextXMagnitude * 0.6f;
                    zComponent = -nextXMagnitude * 0.25f;
                    break;
                case SubtleGameManager.TaskTypeVal.Trials:
                    yComponent = -nextXMagnitude * 0.7f;
                    zComponent = -nextXMagnitude * 0.15f;
                    break;
            }

            // Calculate translation vector
            var desiredTranslation = transform;
            desiredTranslation.localPosition = new Vector3(xComponent, yComponent, zComponent);

            // Place the origin of the sim box at position of the center eye anchor
            simulation.position = centreEyeAnchor.position;

            // Translate the simulation so that the center eye anchor is in the center of the xy plane of the sim box
            simulation.Translate(desiredTranslation.position - simulation.position);
        }
    }
}
