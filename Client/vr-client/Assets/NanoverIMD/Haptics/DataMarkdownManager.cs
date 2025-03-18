using Nanover.Frame.Event;
using Nanover.Frame;
using Nanover.Visualisation;
using NanoverImd.Interaction;
using System.Collections;
using System.Collections.Generic;
using System.Xml;
using UnityEngine;
using System.IO;
using Oculus.Haptics;
using Oculus.Interaction.Input;

namespace GluhutUserTest
{
    public class DataMarkdownManager : MonoBehaviour
    {
        private StreamWriter csvWriter;
        [SerializeField] private InteractableScene interactableScene;
        private SynchronisedFrameSource _frameSource;
        private readonly string[] targetKeys = new string[]
        {
            "energy.kinetic",
            "forces.user.work_done",
            "energy.potential",
            "energy.user.total"
        };

        private void Start()
        {

            _frameSource = interactableScene.GetFrameSource();
            _frameSource.FrameChanged += Haptic;
            string filePath = Path.Combine(Application.persistentDataPath, "haptic_dataMinimizeEnergy0225.csv");
            Debug.Log(Application.persistentDataPath);
            csvWriter = new StreamWriter(filePath, false);


            string header = "timestamp";
            foreach (string key in targetKeys)
            {
                header += $",{key}";
            }
            csvWriter.WriteLine(header);
            csvWriter.Flush();

        }

        private void Haptic(IFrame frame, FrameChanges changes)
        {
            var data = (frame as Frame)?.Data;
            if (data == null) return;


            string timestamp = Time.time.ToString("F3");


            string csvLine = timestamp;


            foreach (string key in targetKeys)
            {
                if (data.TryGetValue(key, out object value))
                {
                    csvLine += $",{value}";
                    Debug.Log("Key is :" + key + ", Value is " + value);
                }
                else
                {
                    csvLine += ",null";
                    Debug.Log("null appear");
                }
            }


            csvWriter.WriteLine(csvLine);
            csvWriter.Flush();
        }

        private void OnDestroy()
        {
            if (csvWriter != null)
            {
                csvWriter.Close();
                csvWriter = null;
            }
        }
    }
}

