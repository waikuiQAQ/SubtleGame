using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Oculus.Haptics;


namespace GluhutUserTest
{
    public class HapticsManager : MonoBehaviour
    {
        private HapticClipPlayer hapticClipPlayer;
        // Start is called before the first frame update
        void Start()
        {

        }

        // Update is called once per frame
        void Update()
        {

        }

        public void ActivateHaptic(float amplitude, float frequency)
        {
            

            hapticClipPlayer.amplitude = amplitude;
            hapticClipPlayer.frequencyShift = frequency;
        }
    }
}

