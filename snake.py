import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# GAME Window
window = tkinter.Tk()
window.title("Snake Game")
window.resizable(False, False)

difficulty = None

# Center The Window
window_width = WINDOW_WIDTH
window_height = WINDOW_HEIGHT
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Global Variables
snake = None
food = None
snake_body = []
velocityX = 0
velocityY = 0
game_over = False
score = 0

# Init Canvas
canvas = tkinter.Canvas(window, bg='black', width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)

def change_direction(event):
    global velocityX, velocityY, game_over

    if (game_over):
        return

    if (event.keysym == 'Up' and velocityY != 1):
        velocityX = 0 
        velocityY = -1
    elif (event.keysym == 'Down' and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif (event.keysym == 'Left' and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif (event.keysym == 'Right' and velocityX != -1):
        velocityX = 1
        velocityY = 0

def move():
    global snake, food, snake_body, game_over, score, difficulty

    if (game_over):
        return
    
    if difficulty != 'Easy':
        if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
            game_over = True
            return
        
        for tile in snake_body:
            if (snake.x == tile.x and snake.y == tile.y):
                game_over = True
                return
    else:
        if snake.x < 0:
            snake.x = WINDOW_WIDTH
        elif snake.x >= WINDOW_WIDTH:
            snake.x = 0
        elif snake.y < 0:
            snake.y = WINDOW_HEIGHT
        elif snake.y >= WINDOW_HEIGHT:
            snake.y = 0

    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1

    for i in range(len(snake_body) -1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            previous_tile = snake_body[i-1]
            tile.x = previous_tile.x
            tile.y = previous_tile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def landing_page():
    landing_frame = tkinter.Frame(window, bg='black', width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    landing_frame.pack(fill='both', expand=True)

    title_label = tkinter.Label(landing_frame, text='Snake Game', font='Arial 24', fg='white', bg='black')
    title_label.pack(pady=20)

    difficulty_label = tkinter.Label(landing_frame, text='Choose A Difficulty', font='Arial 16', fg='white', bg='black')
    difficulty_label.pack(pady=10)

    easy_button = tkinter.Button(landing_frame, text='Easy', font='Arial 14', command=lambda: start_game('Easy'))
    easy_button.pack(pady=5)

    medium_button = tkinter.Button(landing_frame, text='Medium', font='Arial 14', command=lambda: start_game('Medium'))
    medium_button.pack(pady=5)

    hard_button = tkinter.Button(landing_frame, text='Hard', font='Arial 14', command=lambda: start_game('Hard'))
    hard_button.pack(pady=5)

def start_game(selected_difficulty):
    global difficulty, snake, food, snake_body, velocityX, velocityY, game_over, score

    difficulty = selected_difficulty

    for widget in window.winfo_children():
        widget.destroy()

    canvas = tkinter.Canvas(window, bg='black', width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
    canvas.pack()

    window.bind('<KeyRelease>', change_direction)

    # Init Game
    snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
    food = Tile(random.randint(0, COLS-1) * TILE_SIZE, random.randint(0, ROWS-1) * TILE_SIZE)
    snake_body = []
    velocityX = 0
    velocityY = 0
    game_over = False
    score = 0

    window.update()

    def draw():
        global snake, food, snake_body, game_over, score

        move()

        canvas.delete('all')

        # Draw Food
        canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill='red')

        # Draw Snake
        canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill='lime green')

        for tile in snake_body:
            canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill='lime green')
        
        if (game_over):
            canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font='Arial 20', text='Game Over.', fill='white')
            canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 30, font='Arial 16', text=f'Score: {score}', fill='white')
            canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 60, font='Arial 12', text='Press Space To Start New Game', fill='white')
            def new_game(event):
                if event.keysym == 'space':
                    canvas.destroy()
                    landing_page()
                    window.unbind('<KeyRelease>', new_game)
            window.bind('<KeyRelease>', new_game)
        else:
            canvas.create_text(30, 20, font='Arial 10', text=f'Score: {score}', fill='white')

        if (difficulty == 'Easy'):
            window.after(100, draw)
        elif (difficulty == 'Medium'):
            window.after(75, draw)
        elif (difficulty == 'Hard'):
            window.after(50, draw)
    
    draw()

landing_page()

# Listener
window.bind('<KeyRelease>', change_direction)

window.mainloop()
