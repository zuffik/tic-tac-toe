using System;
using System.Collections;
using System.Collections.Generic;
using JetBrains.Annotations;
using UnityEngine;
using UnityEngine.SceneManagement;

/**
 * I know, this is spaghetti code
 */
public class HudController : MonoBehaviour
{
    private Camera _camera;
    private Focusable _focused;
    private int _focusedIndex = 0;
    public float rotationSpeed;
    private Transform _lookTarget;
    private int _size = 0;

    public GameObject[] stage1Items;
    public GameObject[] stage2Items;
    private int stage;

    private bool _downPressedDown;
    private bool _upPressedDown;
    private bool _clickPressedDown;
    private bool _leftPressedDown;
    private bool _rightPressedDown;
    private SliderItemController _toWin;
    private CellType _gameCellType;

    // Start is called before the first frame update
    void Start()
    {
        _camera = gameObject.GetComponent<Camera>();
        for (var i = 0; i < stage1Items.Length; i++)
        {
            SetupItem(stage1Items[i], i);
        }

        for (var i = 0; i < stage2Items.Length; i++)
        {
            SetupItem(stage2Items[i], i);
        }

        _toWin = GameObject.Find("ToWin").GetComponent<SliderItemController>();
        _size = GameObject.Find("BoardSize").GetComponent<SliderItemController>().value;

        SetStage(1);

        SceneManager.sceneLoaded += (scene, mode) =>
        {
            if (scene.name != "MainScene") return;
            var toWin = _toWin.value;
            var size = _size;
            var player = _gameCellType;
            var gameCtrl = GameObject.Find("Game").GetComponent<GameController>();
            gameCtrl.toWin = toWin;
            gameCtrl.player = player;
            GameObject.Find("Grid").GetComponent<Grid>().size = size;
        };
    }

    private void SetStage(int stage)
    {
        _focused = null;
        _focusedIndex = 0;
        this.stage = stage;
        foreach (var item in stage1Items)
        {
            item.SetActive(stage == 1);
        }

        foreach (var item in stage2Items)
        {
            item.SetActive(stage != 1);
        }

        Focus(_focusedIndex);
    }

    private void SetupItem(GameObject item, int i)
    {
        item.transform.position = new Vector3(0, -2 * i, -0.2f);
    }

    private GameObject[] CurrentStageItems()
    {
        return stage == 1 ? stage1Items : stage2Items;
    }

    // Update is called once per frame
    void Update()
    {
        RotateLookingObject();
        if (Physics.Raycast(_camera.transform.position, _camera.transform.forward, out var hit))
        {
            var ctrl = hit.transform.gameObject.GetComponent<Focusable>();
            if (ctrl)
            {
                if (ctrl.CanFocus)
                {
                    BlurAll();
                    ctrl.Focus();
                }

                _focused = ctrl;
            }
            else
            {
                BlurAll();
            }
        }

        var down = Input.GetAxis("Vertical") < -0.0001f;
        if (!_downPressedDown && down)
        {
            _downPressedDown = true;
            Focus(Math.Min(_focusedIndex + 1, CurrentStageItems().Length - 1));
        }

        if (!down && _downPressedDown)
        {
            _downPressedDown = false;
        }

        var up = Input.GetAxis("Vertical") > 0.0001f;
        if (!_upPressedDown && up)
        {
            _upPressedDown = true;
            Focus(Math.Max(_focusedIndex - 1, 0));
        }

        if (!up && _upPressedDown)
        {
            _upPressedDown = false;
        }

        var left = Input.GetAxis("Horizontal") < -0.0001f;
        if (!_leftPressedDown && left)
        {
            _leftPressedDown = true;
            if (_focused.TryGetComponent<SliderItemController>(out var slider))
            {
                slider.Decrement();
                if (slider.gameObject.name == "BoardSize")
                {
                    _size = slider.value;
                    _toWin.SetMax(slider.value);
                }
            }
        }

        if (!left && _leftPressedDown)
        {
            _leftPressedDown = false;
        }

        var right = Input.GetAxis("Horizontal") > 0.0001f;
        if (!_rightPressedDown && right)
        {
            _rightPressedDown = true;
            if (_focused.TryGetComponent<SliderItemController>(out var slider))
            {
                slider.Increment();

                if (slider.gameObject.name == "BoardSize")
                {
                    _size = slider.value;
                    _toWin.SetMax(slider.value);
                }
            }
        }

        if (!right && _rightPressedDown)
        {
            _rightPressedDown = false;
        }

        var click = Math.Abs(Input.GetAxis("Fire1")) > 0.0001f || Input.GetKey(KeyCode.Return);
        if (!_clickPressedDown && click && _focused && _focused.TryGetComponent<ButtonController>(out var btn))
        {
            _clickPressedDown = true;
            switch (btn.id)
            {
                case "exit":
                    Application.Quit();
                    break;
                case "new-game":
                    SetStage(2);
                    break;
                case "start-game-x":
                case "start-game-o":
                    _gameCellType = btn.id == "start-game-x" ? CellType.X : CellType.O;
                    SceneManager.LoadScene("MainScene");
                    break;
            }
        }

        if (!click && _clickPressedDown)
        {
            _clickPressedDown = false;
        }
    }

    private void BlurAll()
    {
        foreach (var item in CurrentStageItems())
        {
            item.GetComponent<Focusable>().Blur();
        }
    }

    private void Focus(int index)
    {
        _focusedIndex = index;
        _lookTarget = CurrentStageItems()[index].transform;
    }

    void RotateLookingObject()
    {
        if (!_lookTarget) return;
        var direction = _lookTarget.position - _camera.transform.position;
        if (direction == Vector3.zero) return;
        var rotation = Quaternion.LookRotation(direction);
        _camera.transform.rotation =
            Quaternion.Slerp(_camera.transform.rotation, rotation, rotationSpeed * Time.deltaTime);
    }
}