using System;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class SliderItemController : MonoBehaviour
{
    public int min;
    public int max;
    public int value;
    private TextMeshPro _value;

    private void Start()
    {
        _value = transform.Find("Value").GetComponent<TextMeshPro>();
        SetValue(value);
    }

    public void SetValue(int value)
    {
        this.value = value;
        _value.SetText(value.ToString());
    }

    public void Increment()
    {
        SetValue(Math.Min(max, value + 1));
    }

    public void Decrement()
    {
        SetValue(Math.Max(0, value - 1));
    }

    public void SetMax(int max)
    {
        this.max = max;
        SetValue(Math.Min(max, value));
    }

    public void SetMin(int min)
    {
        this.min = min;
        SetValue(Math.Max(min, value));
    }
}