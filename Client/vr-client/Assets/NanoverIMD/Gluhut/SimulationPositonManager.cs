using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace GluhutUserTest 
{
    public class SimulationPositonManager : MonoBehaviour
    {
        [SerializeField]private Transform headsetTransform;
        [SerializeField]private Transform simulationTransform;
        private void Start()
        {
            SetSimulationTransform();
        }
        public void SetSimulationTransform()
        {
            SetSimulationPosition();
            SetSimulationScale();
        }

        void SetSimulationPosition()
        {
            
            simulationTransform.position = new Vector3 (0, 0, 0);
        }

        void SetSimulationScale()
        {
            simulationTransform.localScale = new Vector3(0.4f, 0.4f, 0.4f);
        }
    }
}

