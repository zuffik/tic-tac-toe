using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public Camera camera;
    public int offset;
    public GameObject game;

    private GameController _game;
    private bool _assignerPressedDown;

    // Start is called before the first frame update
    void Start()
    {
        gameObject.transform.position = new Vector3(0, 0, GameObject.Find("Grid").GetComponent<Grid>().size * -offset);
        _game = game.GetComponent<GameController>();
    }

    // Update is called once per frame
    void Update()
    {
        if (Physics.Raycast(camera.transform.position, camera.transform.forward, out var hit)) {
            var hitObject = hit.transform.gameObject;
            try
            {
                var cell = hitObject.GetComponent<Cell>();
                _game.HighlightCell(cell.I, cell.J, cell.K);
            }
            catch (MissingComponentException e)
            {
                // pass
            }
        }
        
        var assigner = Math.Abs(Input.GetAxis("Fire3")) > 0.0001f;
        if (!_assignerPressedDown && assigner)
        {
            _assignerPressedDown = true;
            _game.MovePlayerToHighlightedCell();
        }

        if (!assigner && _assignerPressedDown)
        {
            _assignerPressedDown = false;
        }
    }
}
