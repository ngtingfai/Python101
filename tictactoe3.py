from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Tic Tac Toe vs Computer3</title>
  <style>
    body { font-family: Arial, sans-serif; display: flex; flex-direction: column; align-items: center; margin: 40px; }
    h1 { margin-bottom: 10px; }
    #board { display: grid; grid-template-columns: repeat(3, 100px); grid-template-rows: repeat(3, 100px); gap: 5px; }
    .cell { display: flex; align-items: center; justify-content: center; font-size: 3rem; background: #f0f0f0; cursor: pointer; }
    .cell:hover { background: #e0e0e0; }
    #status { margin-top: 20px; font-size: 1.2rem; }
    button { margin-top: 15px; padding: 10px 18px; font-size: 1rem; }
  </style>
</head>
<body>
  <h1>Tic Tac Toe vs Computer3</h1>
  <div id="board"></div>
  <div id="status">Your turn. You are X.</div>
  <button id="reset">Reset Game</button>

  <script>
    const boardEl = document.getElementById('board');
    const statusEl = document.getElementById('status');
    const resetBtn = document.getElementById('reset');
    let board = Array(9).fill('');
    let human = 'X';
    let computer = 'O';
    let gameOver = false;

    const winningLines = [
      [0, 1, 2], [3, 4, 5], [6, 7, 8],
      [0, 3, 6], [1, 4, 7], [2, 5, 8],
      [0, 4, 8], [2, 4, 6]
    ];

    function renderBoard() {
      boardEl.innerHTML = '';
      board.forEach((value, index) => {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.textContent = value;
        cell.addEventListener('click', () => handleClick(index));
        boardEl.appendChild(cell);
      });
    }

    function handleClick(index) {
      if (gameOver || board[index]) return;
      board[index] = human;
      renderBoard();
      if (checkWin(human)) {
        statusEl.textContent = 'You win!';
        gameOver = true;
        return;
      }
      if (board.every(cell => cell)) {
        statusEl.textContent = 'It is a tie!';
        gameOver = true;
        return;
      }
      statusEl.textContent = 'Computer is thinking...';
      setTimeout(() => {
        computerMove();
        renderBoard();
        if (checkWin(computer)) {
          statusEl.textContent = 'Computer wins!';
          gameOver = true;
        } else if (board.every(cell => cell)) {
          statusEl.textContent = 'It is a tie!';
          gameOver = true;
        } else {
          statusEl.textContent = 'Your turn. You are X.';
        }
      }, 250);
    }

    function computerMove() {
      const move = chooseBestMove();
      if (move !== null) {
        board[move] = computer;
      }
    }

    function isHorizontalOrVertical(line) {
      return !(line[0] === 0 && line[1] === 4 && line[2] === 8) &&
             !(line[0] === 2 && line[1] === 4 && line[2] === 6);
    }

    function createsNonDiagonalThreat(index) {
      const copy = [...board];
      copy[index] = computer;
      return winningLines.some(line => {
        if (!isHorizontalOrVertical(line)) return false;
        const computerCount = line.filter(i => copy[i] === computer).length;
        const emptyCount = line.filter(i => copy[i] === '').length;
        return computerCount === 2 && emptyCount === 1;
      });
    }

    function chooseBestMove() {
      const emptyIndexes = board.map((value, index) => value === '' ? index : null).filter(index => index !== null);
      if (!emptyIndexes.length) return null;

      // Win if possible
      for (const index of emptyIndexes) {
        const copy = [...board];
        copy[index] = computer;
        if (checkWinForBoard(copy, computer)) {
          return index;
        }
      }

      // Block human win
      for (const index of emptyIndexes) {
        const copy = [...board];
        copy[index] = human;
        if (checkWinForBoard(copy, human)) {
          return index;
        }
      }

      // Prioritize threatening non-diagonal wins
      const threatMoves = emptyIndexes.filter(index => createsNonDiagonalThreat(index));
      if (threatMoves.length) {
        return threatMoves[0];
      }

      // Prefer center
      if (board[4] === '') return 4;

      // Prefer corners
      const corners = [0, 2, 6, 8].filter(i => board[i] === '');
      if (corners.length) return corners[Math.floor(Math.random() * corners.length)];

      // Otherwise choose a random empty square
      return emptyIndexes[Math.floor(Math.random() * emptyIndexes.length)];
    }

    function checkWin(player) {
      return winningLines.some(line => line.every(index => board[index] === player));
    }

    function checkWinForBoard(testBoard, player) {
      return winningLines.some(line => line.every(index => testBoard[index] === player));
    }

    function resetGame() {
      board = Array(9).fill('');
      gameOver = false;
      statusEl.textContent = 'Your turn. You are X.';
      renderBoard();
    }

    resetBtn.addEventListener('click', resetGame);
    renderBoard();
  </script>
</body>
</html>
'''

@app.route('/')
def play_tictactoe():
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    app.run(debug=True)
