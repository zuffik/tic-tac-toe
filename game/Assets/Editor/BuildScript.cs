using System;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;

public class BuildScript
{
    static void PerformBuild()
    {
        var buildDirectory = Environment.CurrentDirectory + Path.DirectorySeparatorChar + "Build" + Path.DirectorySeparatorChar;
        Debug.Log(buildDirectory);
        BuildPipeline.BuildPlayer(
            new[] {"Assets/Scenes/MenuScene.unity", "Assets/Scenes/MainScene.unity"},
            buildDirectory + "game.exe",
            BuildTarget.StandaloneWindows64,
            BuildOptions.None
        );
        EditorApplication.Exit(Directory.Exists(buildDirectory) ? 0 : 1);
    }
}