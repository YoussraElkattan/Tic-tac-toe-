import tkinter as tk
import heapq

def is_safe(board, row, col):
    for i in range(row):
        if board[i] == col or abs(board[i] - col) == abs(i - row):
            return False
    return True

def heuristic(board):
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def astar_n_queens(n):
    initial_state = [-1] * n
    priority_queue = [(0, initial_state)]
    g_values = {tuple(initial_state): 0}
    
    while priority_queue:
        f, current_state = heapq.heappop(priority_queue)
        if current_state[-1] != -1:
            return current_state
        for row in range(n):
            if current_state[row] == -1:
                for col in range(n):
                    if is_safe(current_state, row, col):
                        child_state = current_state[:]
                        child_state[row] = col
                        child_state_tuple = tuple(child_state)
                        g_value = g_values[tuple(current_state)] + 1
                        h_value = heuristic(child_state)
                        f_value = g_value + h_value
                        if child_state_tuple not in g_values or g_value < g_values[child_state_tuple]:
                            g_values[child_state_tuple] = g_value
                            heapq.heappush(priority_queue, (f_value, child_state))
    return None

def draw_board(board):
    canvas.delete("queens")
    for row, col in enumerate(board):
        x1, y1 = col * cell_size, row * cell_size
        x2, y2 = (col + 1) * cell_size, (row + 1) * cell_size
        canvas.create_oval(x1, y1, x2, y2, fill="red", tags="queens")

def solve_and_draw():
    n = int(entry.get())
    result = astar_n_queens(n)
    
    if result:
        draw_board(result)
    else:
        canvas.delete("queens")
        canvas.create_text(cell_size * n // 2, cell_size * n // 2, text="No solution", fill="red")

app = tk.Tk()
app.title("N-Queens Solver")

frame = tk.Frame(app)
frame.pack()

label = tk.Label(frame, text="Enter the board size (N):")
label.pack()

entry = tk.Entry(frame)
entry.pack()

solve_button = tk.Button(frame, text="Solve", command=solve_and_draw)
solve_button.pack()

canvas = tk.Canvas(app, width=400, height=400)
canvas.pack()

cell_size = 400 // 8

for i in range(8):
    for j in range(8):
        x1, y1 = j * cell_size, i * cell_size
        x2, y2 = (j + 1) * cell_size, (i + 1) * cell_size
        color = "white" if (i + j) % 2 == 0 or (i + j) % 2 == 2 else "black"
        canvas.create_rectangle(x1, y1, x2, y2, fill=color)

app.mainloop()
