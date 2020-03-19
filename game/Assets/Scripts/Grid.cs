using System;
using UnityEngine;

public class Grid : MonoBehaviour
{
    public int size;
    public float rotationSpeed;

    private GameObject _highlighted;
    private GameObject[][][] _grid;
    private int _visibleCellsInDimension;

    private bool _extenderPressedDown;
    private bool _shrinkerPressedDown;

    public CellType[][][] Cells => GetCells();

    // Start is called before the first frame update
    void Start()
    {
        _visibleCellsInDimension = Math.Max(1, size - 2);
        var visibleMin = size / 2 - _visibleCellsInDimension / 2;
        var visibleMax = visibleMin + _visibleCellsInDimension;

        var cell = transform.Find("Cell").gameObject;
        cell.SetActive(false);
        var cellSize = new Vector3(2, 2, 2);
        var offset = -(size / 2f) * cellSize + cellSize / 2f;
        _grid = new GameObject[size][][];
        for (var i = 0; i < size; i++)
        {
            _grid[i] = new GameObject[size][];
            for (var j = 0; j < size; j++)
            {
                _grid[i][j] = new GameObject[size];
                for (var k = 0; k < size; k++)
                {
                    var current = Instantiate(cell, transform, true);
                    current.transform.position = offset + new Vector3(
                        cellSize.x * i,
                        cellSize.y * j,
                        cellSize.z * k
                    );
                    current.SetActive(true);
                    current.GetComponent<Cell>().SetGridPosition(i, j, k);
                    current.GetComponent<Cell>().SetActive(i >= visibleMin && i < visibleMax &&
                                                           j >= visibleMin && j < visibleMax &&
                                                           k >= visibleMin && k < visibleMax);
                    _grid[i][j][k] = current;
                }
            }
        }
    }

    // Update is called once per frame
    void Update()
    {
        var vertical = Input.GetAxis("Vertical") * Time.deltaTime * rotationSpeed;
        var horizontal = Input.GetAxis("Horizontal") * Time.deltaTime * rotationSpeed;
        transform.RotateAround(new Vector3(0, 0, 0), Vector3.left, vertical);
        transform.RotateAround(new Vector3(0, 0, 0), Vector3.up, horizontal);
        var extender = Math.Abs(Input.GetAxis("Fire1")) > 0.0001f;
        if (!_extenderPressedDown && extender)
        {
            _extenderPressedDown = true;
            Extend();
        }

        if (!extender && _extenderPressedDown)
        {
            _extenderPressedDown = false;
        }

        var shrinker = Math.Abs(Input.GetAxis("Fire2")) > 0.0001f;
        if (!_shrinkerPressedDown && shrinker)
        {
            _shrinkerPressedDown = true;
            Shrink();
        }

        if (!shrinker && _shrinkerPressedDown)
        {
            _shrinkerPressedDown = false;
        }
    }

    public void Assign(CellType cellType)
    {
        _highlighted.GetComponent<Cell>().SetCellType(cellType);
    }

    public bool CanAssign()
    {
        return _highlighted != null;
    }

    public bool CanHighlight(int i, int j, int k)
    {
        return _grid[i][j][k].GetComponent<Cell>().CellType == CellType.Empty || _grid[i][j][k].GetComponent<Cell>().CellType == CellType.Highlight;
    }

    private void Shrink()
    {
        ChangeGridSize(-2);
    }

    private void Extend()
    {
        ChangeGridSize(2);
    }

    private void ChangeGridSize(int number)
    {
        _visibleCellsInDimension = Math.Max(Math.Min(size, _visibleCellsInDimension + number), 2 - size % 2);
        var visibleMin = size / 2 - _visibleCellsInDimension / 2;
        var visibleMax = visibleMin + _visibleCellsInDimension;
        for (var i = 0; i < size; i++)
        {
            for (var j = 0; j < size; j++)
            {
                for (var k = 0; k < size; k++)
                {
                    _grid[i][j][k].GetComponent<Cell>().SetActive(i >= visibleMin && i < visibleMax &&
                                                                  j >= visibleMin && j < visibleMax &&
                                                                  k >= visibleMin && k < visibleMax);
                }
            }
        }
    }

    public void HighlightCell(int iPos, int jPos, int kPos)
    {
        for (var i = 0; i < size; i++)
        {
            for (var j = 0; j < size; j++)
            {
                for (var k = 0; k < size; k++)
                {
                    if (_grid[i][j][k].GetComponent<Cell>().CellType == CellType.Highlight)
                    {
                        _grid[i][j][k].GetComponent<Cell>().SetCellType(CellType.Empty);
                    }
                }
            }
        }

        _highlighted = _grid[iPos][jPos][kPos];
        var cell = _highlighted.GetComponent<Cell>();
        if (cell.CellType == CellType.Empty || cell.CellType == CellType.Highlight)
        {
            cell.SetCellType(CellType.Highlight);
        }
        else
        {
            _highlighted = null;
        }
    }

    private CellType[][][] GetCells()
    {
        var result = new CellType[size][][];
        for (var i = 0; i < size; i++)
        {
            result[i] = new CellType[size][];
            for (var j = 0; j < size; j++)
            {
                result[i][j] = new CellType[size];
                for (var k = 0; k < size; k++)
                {
                    result[i][j][k] = _grid[i][j][k].GetComponent<Cell>().CellType;
                }
            }
        }

        return result;
    }
}