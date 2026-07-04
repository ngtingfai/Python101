from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Tic Tac Toe</title>
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
  <h1>Tic Tac Toe</h1>
  <div id="board"></div>
  <div id="status">Click any square to start playing.</div>
  <button id="reset">Reset Game</button>

  <script>
    const boardEl = document.getElementById('board');
    const statusEl = document.getElementById('status');
    const resetBtn = document.getElementById('reset');
    let board = Array(9).fill('');
    let currentPlayer = 'X';
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
      board[index] = currentPlayer;
      if (checkWin(currentPlayer)) {
        statusEl.textContent = `${currentPlayer} wins!`;
        gameOver = true;
      } else if (board.every(cell => cell)) {
        statusEl.textContent = 'It is a tie!';
        gameOver = true;
      } else {
        currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
        statusEl.textContent = `Current player: ${currentPlayer}`;
      }
      renderBoard();
    }

    function checkWin(player) {
      return winningLines.some(line => line.every(index => board[index] === player));
    }

    function resetGame() {
      board = Array(9).fill('');
      currentPlayer = 'X';
      gameOver = false;
      statusEl.textContent = 'Click any square to start playing.';
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
