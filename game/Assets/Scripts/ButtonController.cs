using System;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class ButtonController : MonoBehaviour
{
    public string label;
    public string id;

    private MeshRenderer _planeRenderer;
    private Material _buttonHighlightedMaterial;
    private Material _buttonMaterial;
    
    private readonly Vector3 _largerScale = new Vector3(1.1f, 1.1f, 1.1f);
    private readonly Vector3 _normalScale = new Vector3(1f, 1f, 1f);

    private void Start()
    {
        gameObject.transform.Find("Label").GetComponent<TextMeshPro>().SetText(label);
        _planeRenderer = gameObject.transform.Find("Plane").GetComponent<MeshRenderer>();
        _buttonHighlightedMaterial = Resources.Load<Material>("Materials/ButtonHighlightedMaterial");
        _buttonMaterial = Resources.Load<Material>("Materials/ButtonMaterial");
    }

    public void Focus()
    {
        _planeRenderer.material = _buttonHighlightedMaterial;
        transform.localScale = _largerScale;
    }

    public void Blur()
    {
        _planeRenderer.material = _buttonMaterial;
        transform.localScale = _normalScale;
    }
}
