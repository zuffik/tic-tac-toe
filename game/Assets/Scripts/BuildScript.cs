using System;
using System.IO;
using UnityEditor;
using UnityEngine;

public class BuildScript
{
    static void PerformBuild()
    {
        var buildDirectory = Environment.CurrentDirectory + Path.PathSeparator + "Build" + Path.PathSeparator;
        var winBuildDirectory = buildDirectory + "Win" + Path.PathSeparator;
        var webGLBuildDirectory = buildDirectory + "WebGL" + Path.PathSeparator;
        Directory.CreateDirectory(buildDirectory);
        Directory.CreateDirectory(winBuildDirectory);
        Directory.CreateDirectory(webGLBuildDirectory);
        Debug.Log(buildDirectory);
        Debug.Log(winBuildDirectory);
        Debug.Log(winBuildDirectory);
        Debug.Log("*** Building Windows ***");
        var report = BuildPipeline.BuildPlayer(
            new[] {"Assets/MainScene.unity"},
            winBuildDirectory + "game.exe",
            BuildTarget.StandaloneWindows64,
            BuildOptions.None
        );
        Debug.Log("Windows report:");
        Debug.Log(report);
        Debug.Log(report.files);
        

        Debug.Log("*** Building WebGL ***");
        report = BuildPipeline.BuildPlayer(
            new[] {"Assets/MainScene.unity"},
            webGLBuildDirectory,
            BuildTarget.WebGL,
            BuildOptions.None
        );
        Debug.Log("WebGL report:");
        Debug.Log(report);
        Debug.Log(report.files);


    }
}