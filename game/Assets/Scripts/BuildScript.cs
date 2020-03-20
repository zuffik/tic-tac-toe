using System;
using UnityEditor;
using UnityEngine;

public class BuildScript
{
    static void PerformBuild()
    {
        Debug.Log(Environment.CurrentDirectory);
        Debug.Log("*** Building Windows ***");
        var report = BuildPipeline.BuildPlayer(
            new[] {"Assets/MainScene.unity"},
            Environment.CurrentDirectory + "/Build/Win/game.exe",
            BuildTarget.StandaloneWindows64,
            BuildOptions.None
        );
        Debug.Log("Windows report:");
        Debug.Log(report);

        Debug.Log("*** Building WebGL ***");
        report = BuildPipeline.BuildPlayer(
            new[] {"Assets/MainScene.unity"},
            Environment.CurrentDirectory + "/Build/WebGL/",
            BuildTarget.WebGL,
            BuildOptions.None
        );
        Debug.Log("WebGL report:");
        Debug.Log(report);


    }
}