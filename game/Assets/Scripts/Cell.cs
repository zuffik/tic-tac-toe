using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public enum CellType
{
    X,
    O,
    Empty,
    Highlight
}

public class Cell : MonoBehaviour
{
    private CellType _cellType = CellType.Empty;
    public CellType CellType => _cellType;

    public GameObject x;
    public GameObject o;
    public GameObject highlight;
    public GameObject[] bars;

    private int _i;
    private int _j;
    private int _k;

    public int I => _i;
    public int J => _j;
    public int K => _k;

    public void SetGridPosition(int i, int j, int k)
    {
        _i = i;
        _j = j;
        _k = k;
    }

    public void SetCellType(CellType cellType)
    {
        _cellType = cellType;
        x.SetActive(cellType == CellType.X);
        o.SetActive(cellType == CellType.O);
        highlight.SetActive(cellType == CellType.Highlight);
    }

    private void SetOpacity(GameObject obj, float opacity)
    {
        var color = obj.GetComponent<Renderer>().material.color;
        color.a = opacity;
        obj.GetComponent<Renderer>().material.color = color;
    }

    public void SetOpacity(float opacity)
    {
        foreach (var obj in bars)
        {
            SetOpacity(obj, opacity);
        }
        SetOpacity(highlight, opacity);

        SetOpacity(x.transform.Find("X1").gameObject, opacity);
        SetOpacity(x.transform.Find("X2").gameObject, opacity);
        SetOpacity(x.transform.Find("X3").gameObject, opacity);
        SetOpacity(x.transform.Find("X4").gameObject, opacity);

        SetOpacity(o.transform.Find("XTorus").Find("group_0_16448250").gameObject, opacity);
        SetOpacity(o.transform.Find("YTorus").Find("group_0_16448250").gameObject, opacity);
        SetOpacity(o.transform.Find("ZTorus").Find("group_0_16448250").gameObject, opacity);
    }

    public void SetActive(bool active)
    {
        SetOpacity(active ? 1f : 0f);
        GetComponent<Collider>().enabled = active;
    }
}