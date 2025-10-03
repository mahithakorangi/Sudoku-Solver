

from flask import Flask, render_template, request, redirect, url_for
import json
import os

# Explicitly set the template folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
app = Flask(__name__, template_folder=TEMPLATE_DIR)

# --- Backend: Sudoku Solver ---
def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:
            return False
    for x in range(9):
        if board[x][col] == num:
            return False
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[startRow + i][startCol + j] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    board = []
    for i in range(9):
        row = []
        for j in range(9):
            val = request.form.get(f'cell{i}_{j}', '')
            try:
                num = int(val)
                if 1 <= num <= 9:
                    row.append(num)
                else:
                    row.append(0)
            except:
                row.append(0)
        board.append(row)
    original = [r[:] for r in board]
    if solve_sudoku(board):
        return render_template('solution.html', solution=board)
    else:
        return '<h3>No solution exists. <a href="/">Try again</a></h3>'

@app.route('/record', methods=['POST'])
def record():
    solution_json = request.form.get('solution')
    solution = json.loads(solution_json)
    # Save to file
    record_path = os.path.join(os.path.dirname(__file__), 'recorded_solution.txt')
    with open(record_path, 'a') as f:
        f.write(json.dumps(solution) + '\n')
    return '<h3>Solution recorded! <a href="/">Back to Home</a></h3>'

if __name__ == '__main__':
    # Debug: print template folder and files
    print(f"Template folder: {TEMPLATE_DIR}")
    print("Files in template folder:", os.listdir(TEMPLATE_DIR))
    app.run(debug=True)