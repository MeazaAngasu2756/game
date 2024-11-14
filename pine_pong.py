import tkinter as tk
from tkinter import messagebox

# Game constants
WIDTH, HEIGHT = 600, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_SIZE = 20

# Game variables
paddle_speed = 20
ball_speed_x, ball_speed_y = 4, -4
score = 0
lives = 3
game_paused = False

# Create main window
window = tk.Tk()
window.title("Enhanced Ping Pong Game")
window.resizable(False, False)

# Create canvas for game
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Paddle and Ball
paddle = canvas.create_rectangle(WIDTH / 2 - PADDLE_WIDTH / 2, HEIGHT - PADDLE_HEIGHT - 20,
                                 WIDTH / 2 + PADDLE_WIDTH / 2, HEIGHT - 20, fill="blue")
ball = canvas.create_oval(WIDTH / 2 - BALL_SIZE / 2, HEIGHT / 2 - BALL_SIZE / 2,
                          WIDTH / 2 + BALL_SIZE / 2, HEIGHT / 2 + BALL_SIZE / 2, fill="red")

# Score and Lives display
score_text = canvas.create_text(50, 20, text="Score: 0", fill="white", font=("Arial", 16))
lives_text = canvas.create_text(WIDTH - 50, 20, text="Lives: 3", fill="white", font=("Arial", 16))

# Difficulty selection
difficulty = messagebox.askquestion("Select Difficulty", "Choose difficulty:\nYes for Hard, No for Easy")
if difficulty == "yes":
    ball_speed_x, ball_speed_y = 6, -6

# Paddle movement function
def move_paddle(event):
    if game_paused:
        return
    x = 0
    if event.keysym == "Left" and canvas.coords(paddle)[0] > 0:
        x = -paddle_speed
    elif event.keysym == "Right" and canvas.coords(paddle)[2] < WIDTH:
        x = paddle_speed
    canvas.move(paddle, x, 0)

# Ball movement and collision function
def move_ball():
    global ball_speed_x, ball_speed_y, score, lives, game_paused

    if game_paused:
        return

    canvas.move(ball, ball_speed_x, ball_speed_y)
    ball_pos = canvas.coords(ball)
    paddle_pos = canvas.coords(paddle)

    # Ball collision with walls
    if ball_pos[0] <= 0 or ball_pos[2] >= WIDTH:
        ball_speed_x = -ball_speed_x
    if ball_pos[1] <= 0:
        ball_speed_y = -ball_speed_y

    # Ball collision with paddle
    if (ball_pos[3] >= paddle_pos[1] and
        paddle_pos[0] < ball_pos[2] < paddle_pos[2]):
        ball_speed_y = -ball_speed_y
        score += 1
        canvas.itemconfig(score_text, text=f"Score: {score}")

    # Ball falls below paddle
    if ball_pos[3] > HEIGHT:
        lives -= 1
        canvas.itemconfig(lives_text, text=f"Lives: {lives}")
        reset_ball()
        if lives == 0:
            game_over()
            return

    # Keep the game running
    window.after(20, move_ball)

# Reset ball position
def reset_ball():
    canvas.coords(ball, WIDTH / 2 - BALL_SIZE / 2, HEIGHT / 2 - BALL_SIZE / 2,
                  WIDTH / 2 + BALL_SIZE / 2, HEIGHT / 2 + BALL_SIZE / 2)

# Pause/Resume game
def toggle_pause(event):
    global game_paused
    game_paused = not game_paused
    if not game_paused:
        move_ball()

# Game Over function
def game_over():
    canvas.create_text(WIDTH / 2, HEIGHT / 2, text="Game Over", fill="white", font=("Arial", 24))
    canvas.create_text(WIDTH / 2, HEIGHT / 2 + 30, text="Press 'R' to Restart", fill="white", font=("Arial", 14))

# Restart game
def restart_game(event):
    global score, lives, game_paused, ball_speed_x, ball_speed_y
    score = 0
    lives = 3
    game_paused = False
    canvas.itemconfig(score_text, text="Score: 0")
    canvas.itemconfig(lives_text, text="Lives: 3")
    reset_ball()
    move_ball()

    
# Bind controls
window.bind("<Left>", move_paddle)
window.bind("<Right>", move_paddle)
window.bind("p", toggle_pause)    # Press 'p' to pause/resume
window.bind("r", restart_game)    # Press 'r' to restart after game over
move_ball()  # Start moving the ball
window.mainloop()




