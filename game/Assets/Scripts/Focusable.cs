using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Focusable : MonoBehaviour
{
    private bool _focused = false;
    public bool CanFocus => !_focused;

    public void Focus()
    {
        if (_focused) return;
        _focused = true;
        if (gameObject.TryGetComponent<ButtonController>(out var ctrl))
        {
            ctrl.Focus();
        }
    }

    public void Blur()
    {
        if (!_focused) return;
        _focused = false;
        if (gameObject.TryGetComponent<ButtonController>(out var ctrl))
        {
            ctrl.Blur();
        }
    }
}
