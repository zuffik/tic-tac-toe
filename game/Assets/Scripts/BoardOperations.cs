using System;
using System.Collections.Generic;
using System.Linq;

public enum Winner
{
    X,
    O,
    Draw
}

enum IndexType
{
    Rows,
    BoardDiagonals,
    SpaceDiagonals
}

public static class BoardOperations
{
    public class Coords : IComparable<Coords>
    {
        public int X { get; set; }
        public int Y { get; set; }
        public int Z { get; set; }

        public int CompareTo(Coords other)
        {
            if (ReferenceEquals(this, other)) return 0;
            if (ReferenceEquals(null, other)) return 1;
            var xComparison = X.CompareTo(other.X);
            if (xComparison != 0) return xComparison;
            var yComparison = Y.CompareTo(other.Y);
            return yComparison != 0 ? yComparison : Z.CompareTo(other.Z);
        }
    }

    public static Winner GetBoardWinner(CellType[][][] board, int toWin)
    {
        return CheckForWinnerRecursively(board, toWin, 0, 0, 0, new List<Coords>());
    }

    private static Winner CheckForWinnerRecursively(CellType[][][] board, int toWin, int x, int y, int z,
        ICollection<Coords> check)
    {
        var size = board.Length;
        if (x + toWin > size || y + toWin > size || z + toWin > size)
        {
            return Winner.Draw;
        }

        var coords = new Coords {X = x, Y = y, Z = z};
        var winner = check.Contains(coords) ? Winner.Draw : GetBoardWinner(board, toWin, x, y, z);
        check.Append(coords);
        if (winner != Winner.Draw) return winner;

        winner = CheckForWinnerRecursively(board, toWin, x + 1, y, z, check);
        if (winner != Winner.Draw) return winner;

        winner = CheckForWinnerRecursively(board, toWin, x, y + 1, z, check);
        if (winner != Winner.Draw) return winner;

        winner = CheckForWinnerRecursively(board, toWin, x, y, z + 1, check);
        if (winner != Winner.Draw) return winner;

        winner = CheckForWinnerRecursively(board, toWin, x + 1, y, z + 1, check);
        if (winner != Winner.Draw) return winner;

        winner = CheckForWinnerRecursively(board, toWin, x + 1, y + 1, z, check);
        if (winner != Winner.Draw) return winner;

        winner = CheckForWinnerRecursively(board, toWin, x, y + 1, z + 1, check);
        if (winner != Winner.Draw) return winner;

        winner = CheckForWinnerRecursively(board, toWin, x + 1, y + 1, z + 1, check);
        if (winner != Winner.Draw) return winner;

        return Winner.Draw;
    }

    private static int ToDecimal(string str, int b)
    {
        var len = str.Length;
        var power = 1;  
        var num = 0; 

        for (var i = len - 1; i >= 0; i--)
        {
            if (int.Parse(str[i].ToString()) >= b)
            {
                throw new Exception($"Invalid number {str} for base {b}");
            }

            num += int.Parse(str[i].ToString()) * power;
            power *= b;
        }

        return num;
    }

    private static Winner GetBoardWinner(CellType[][][] board, int toWin, int x, int y, int z)
    {
        var possibilities = new CellType[(int) Math.Pow(toWin, 2) * 9 + 4][];
        for (var i = 0; i < possibilities.Length; i++)
        {
            possibilities[i] = new CellType[toWin];
            for (var j = 0; j < toWin; j++)
            {
                possibilities[i][j] = CellType.Empty;
            }
        }

        int index;
        for (var i = x; i < x + toWin; i++)
        {
            for (var j = y; j < y + toWin; j++)
            {
                for (var k = z; k < z + toWin; k++)
                {
                    index = PossibilitiesIndex(IndexType.Rows, toWin, i - x, j - y, 0);
                    possibilities[index][k - z] = board[i][j][k];
                    index = PossibilitiesIndex(IndexType.Rows, toWin, i - x, k - z, 1);
                    possibilities[index][j - y] = board[i][j][k];
                    index = PossibilitiesIndex(IndexType.Rows, toWin, j - y, k - z, 2);
                    possibilities[index][i - x] = board[i][j][k];
                    
                    index = PossibilitiesIndex(IndexType.BoardDiagonals, toWin, i - x, j - y, 0);
                    possibilities[index][k - z] = board[i][k][k];
                    index = PossibilitiesIndex(IndexType.BoardDiagonals, toWin, i - x, k - z, 1);
                    possibilities[index][j - y] = board[j][j][k];
                    index = PossibilitiesIndex(IndexType.BoardDiagonals, toWin, j - y, k - z, 2);
                    possibilities[index][i - x] = board[i][j][i];
                    index = PossibilitiesIndex(IndexType.BoardDiagonals, toWin, i - x, j - y, 3);
                    possibilities[index][k - z] = board[i][k][toWin - k - 1 + z];
                    index = PossibilitiesIndex(IndexType.BoardDiagonals, toWin, i - x, k - z, 4);
                    possibilities[index][j - y] = board[j][toWin - j - 1 + y][k];
                    index = PossibilitiesIndex(IndexType.BoardDiagonals, toWin, j - y, k - z, 5);
                    possibilities[index][i - x] = board[toWin - i - 1 + x][j][i];
                }
            }
            index = PossibilitiesIndex(IndexType.SpaceDiagonals, toWin, 0, 0, 0);
            possibilities[index][i - x] = board[i][i][i];
            index = PossibilitiesIndex(IndexType.SpaceDiagonals, toWin, 0, 0, 1);
            possibilities[index][i - x] = board[toWin - i - 1 + x][i][i];
            index = PossibilitiesIndex(IndexType.SpaceDiagonals, toWin, 0, 0, 2);
            possibilities[index][i - x] = board[i][toWin - i - 1 + x][i];
            index = PossibilitiesIndex(IndexType.SpaceDiagonals, toWin, 0, 0, 3);
            possibilities[index][i - x] = board[i][i][toWin - i - 1 + x];
        }

        var results = possibilities.Where(row => row[0] != CellType.Empty && row.All(r => r == row[0])).ToList();
        if (results.Count > 0)
        {
            return results[0][0] == CellType.X ? Winner.X : Winner.O;
        }

        return Winner.Draw;
    }


    private static int PossibilitiesIndex(IndexType index, int toWin, int x, int y, int extra = 0)
    {
        var dec = ToDecimal(string.Join("", new[] {x, y}), toWin);
        switch (index)
        {
            case IndexType.Rows:
                return (int) Math.Pow(toWin, 2) * extra + dec;
            case IndexType.BoardDiagonals:
                return (int) Math.Pow(toWin, 2) * (extra + 3) + dec;
            case IndexType.SpaceDiagonals:
                return (int) Math.Pow(toWin, 2) * 9 + extra;
            default:
                throw new ArgumentOutOfRangeException(nameof(index), index, null);
        }
    }

    public static bool HasAnyMovesLeft(CellType[][][] board)
    {
        return board.Any(t2 => board.Where((t1, j) => board.Where((t, k) => t2[j][k] == CellType.Empty).Any()).Any());
    }
}