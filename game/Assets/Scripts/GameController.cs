using System;
using System.Collections;
using System.IO;
using Cambia.BaseN;
using TensorFlow;
using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;

public class GameController : MonoBehaviour
{
    private static readonly string INPUT_LAYER = "dense_input";
    private static readonly string OUTPUT_LAYER = "out_softmax/Softmax";

    public GameObject grid;
    private Grid _grid;

    public CellType player;
    private CellType _opponent = CellType.O;
    private CellType _onMove;
    private TFGraph _graph;
    private TFSession _session;

    public int toWin;
    private TextMeshPro _text;

    // Start is called before the first frame update
    void Start()
    {
        _grid = grid.GetComponent<Grid>();
        _onMove = player;
        _opponent = player == CellType.X ? CellType.O : CellType.X;

        var file = $"Models/size-{_grid.size}-to-win-{toWin}/model";
        var res = Resources.Load<TextAsset>(file);
        _graph = new TFGraph();
        _graph.Import(res.bytes);
        _session = new TFSession(_graph);

        _text = GameObject.Find("WinnerLoserText").GetComponent<TextMeshPro>();
        _text.gameObject.SetActive(false);
    }

    public void HighlightCell(int i, int j, int k)
    {
        _grid.HighlightCell(i, j, k);
    }

    private void SwitchPlayer()
    {
        _onMove = _onMove == player ? _opponent : player;
        PrintIfGameOver();
    }

    private int GridVectorIndex(int i, int j, int k)
    {
        var input = i.ToString() + j + k;
        return int.Parse(BaseConverter.Convert(
            input,
            new BaseNAlphabet(BaseNAlphabet.Base95.ToString().Substring(0, _grid.size)),
            BaseNAlphabet.Base10
        ));
    }

    private int[] GridIndex(int vectorIndex)
    {
        var result = BaseConverter.Convert(
            vectorIndex.ToString(),
            BaseNAlphabet.Base10,
            new BaseNAlphabet(BaseNAlphabet.Base95.ToString().Substring(0, _grid.size))
        ).PadLeft(3, '0');
        return new[]
        {
            int.Parse(result[0].ToString()),
            int.Parse(result[1].ToString()),
            int.Parse(result[2].ToString())
        };
    }

    private float[] GridHash(CellType[][][] grid)
    {
        var gridVectorSize = (int) Math.Pow(_grid.size, 3);
        var result = new float[gridVectorSize * 3];
        for (var i = 0; i < _grid.size; i++)
        {
            for (var j = 0; j < _grid.size; j++)
            {
                for (var k = 0; k < _grid.size; k++)
                {
                    var index = GridVectorIndex(i, j, k);
                    var cell = grid[i][j][k];
                    var multiplicative = 0;
                    if (cell == _opponent)
                    {
                        multiplicative = 1;
                    } else if (cell == player)
                    {
                        multiplicative = 2;
                    }

                    result[index + gridVectorSize * multiplicative] = 1f;
                }
            }
        }

        return result;
    }

    private void MoveOpponent()
    {
        var hash = GridHash(_grid.Cells);
        var runner = _session.GetRunner();
        runner.AddInput(_graph[INPUT_LAYER][0], new[] {hash});
        runner.Fetch(_graph[OUTPUT_LAYER][0]);
        var result = runner.Run()[0].GetValue() as float[,];

        var outputSize = (int) Math.Pow(_grid.size, 3);
        var max = 0f;
        var maxIndex = -1;
        for (var i = 0; i < outputSize; i++)
        {
            var gi = GridIndex(i);
            if (result[0, i] <= max || !_grid.CanHighlight(gi[0], gi[1], gi[2])) continue;
            max = result[0, i];
            maxIndex = i;
        }

        if (maxIndex < 0) return;
        var index = GridIndex(maxIndex);
        _grid.HighlightCell(index[0], index[1], index[2]);
        _grid.Assign(_onMove);
        SwitchPlayer();
    }

    public void MovePlayerToHighlightedCell()
    {
        if (_onMove != player || !_grid.CanAssign()) return;
        _grid.Assign(_onMove);
        SwitchPlayer();
        MoveOpponent();
    }

    private void PrintIfGameOver()
    {
        var winner = BoardOperations.GetBoardWinner(_grid.Cells, toWin);
        if (winner == Winner.Draw && BoardOperations.HasAnyMovesLeft(_grid.Cells)) return;
        _text.SetText(winner == Winner.Draw ? "Draw" : winner == (player == CellType.X ? Winner.X : Winner.O) ? "You won" : "You lose");
        _text.gameObject.SetActive(true);
        StartCoroutine(WaitAndExit());
    }

    private IEnumerator WaitAndExit()
    {
        yield return new WaitForSeconds(10);
        SceneManager.LoadScene("MenuScene");
    }
}