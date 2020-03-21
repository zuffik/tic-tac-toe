using System;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;

public class BuildScript
{
    static void PerformBuild()
    {
        var buildDirectory = Environment.CurrentDirectory + Path.PathSeparator + "Build" + Path.PathSeparator;
        var winBuildDirectory = buildDirectory + "Win" + Path.PathSeparator;
        var webGLBuildDirectory = buildDirectory + "WebGL" + Path.PathSeparator;
        Debug.Log(buildDirectory);
        Debug.Log(winBuildDirectory);
        Debug.Log(winBuildDirectory);
        Debug.Log("*** Building Windows ***");
        var report = BuildPipeline.BuildPlayer(
            new[] {"Assets/Scenes/MainScene.unity"},
            winBuildDirectory + "game.exe",
            BuildTarget.StandaloneWindows64,
            BuildOptions.None
        );
        Debug.Log("Windows files:");
        foreach (var f in report.files)
        {
            Debug.Log(f.path);
        }
        

        Debug.Log("*** Building WebGL ***");
        report = BuildPipeline.BuildPlayer(
            new[] {"Assets/Scenes/MainScene.unity"},
            webGLBuildDirectory,
            BuildTarget.WebGL,
            BuildOptions.None
        );
        Debug.Log("WebGL files:");
        foreach (var f in report.files)
        {
            Debug.Log(f.path);
        }
        EditorApplication.Exit(Directory.Exists(buildDirectory) ? 0 : 1);
    }
}