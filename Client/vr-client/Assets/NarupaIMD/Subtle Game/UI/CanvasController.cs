using System.Collections.Generic;
using UnityEngine;

namespace NarupaIMD.Subtle_Game.UI
{
    /// <summary>
    /// Class <c>CanvasController</c> holds the CanvasType for each menu canvas. Attach this script to a menu canvas and select the type from the Inspector.
    /// </summary>
    public class CanvasController : MonoBehaviour
    {
        public CanvasType canvasType;

        public List<GameObject> orderedListOfMenus;
    }
}