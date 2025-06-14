import tkinter #graphic interface library
import random #to place food randomly

ROWS = 25       #window is of 25*25 pixels boxes where each tile is consist of 25*25 pixels
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT =  ROWS * TILE_SIZE

class Tile:
    #used for storing x and y position
    def __init__(self,x,y):
        self.x = x
        self.y = y


#game window
window = tkinter.Tk()  #to open window in game
window.resizable(False,False)   #we dont want to change the size of window by user
window.title("Snake Game")  #to give tilte to window

#Adding canvas to the window
canvas  = tkinter.Canvas(window, bg = "black" , width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()     #add canvas to the window

#center the window
#to center the window we need height and width if window as well as computer screen
window_height = window.winfo_height()
window_width = window.winfo_width()
screen_height = window.winfo_screenheight()
screen_width = window.winfo_screenwidth()

window_x = int((screen_width/2)- (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

# f string allows us to inject variable values as string 
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#intialise game
snake = Tile(5*TILE_SIZE , 5*TILE_SIZE) #single tile for snakes head
food = Tile(10*TILE_SIZE , 10*TILE_SIZE)
snake_body = [] #to store multiple snake tiles 
velocityX = 0
velocityY = 0
game_over = False
score = 0

def change_direction(e):    #e = event
    global velocityX,velocityY,game_over

    if(game_over):
        return

    if(e.keysym == "Up" and velocityY != 1):
        velocityY = -1
        velocityX = 0
    elif(e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif(e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0
    elif(e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0

def move():
    global snake,food,snake_body,game_over,score

    if(game_over):
        return

    if(snake.x < 0 or snake.x >WINDOW_WIDTH or snake.y < 0 or snake.y > WINDOW_HEIGHT):
        game_over = True
        return 
    
    for tile in snake_body:
        if(snake.x == tile.x and snake.y == tile.y):
            game_over= True
            return
    #checking for collisons 
    if(snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x ,food.y))
        food.x = random.randint(0,COLS-1) * TILE_SIZE
        food.y = random.randint(0,ROWS -1) * TILE_SIZE
        score += 1

    #for updating snakes body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if(i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX* TILE_SIZE
    snake.y += velocityY* TILE_SIZE


def draw():
    #to draw snake
    global snake , food, snake_body,game_over,score   #using global so that it knows we are using same snake declared before 
    move()

    canvas.delete("all")

    #to create food 
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE , fill = "red")

    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE , fill = "lime green")

    for tile in snake_body:
        canvas.create_rectangle(tile.x ,tile.y , tile.x +TILE_SIZE , tile.y +TILE_SIZE, fill = "lime green")

    if(game_over):
        canvas.create_text(WINDOW_WIDTH/2,WINDOW_HEIGHT/2, font = "Arial 20" , fill="white" , text= f"Game Over : {score}")
    else:
        canvas.create_text(30,20,font="Arial 10" , fill="white" , text = f"Score : {score}")
    
    window.after(150,draw) #100 ms = 1/10 sec basically we want to call draw function after every 100 ms 

draw()


window.bind("<KeyRelease>" , change_direction)
window.mainloop()   #to on our window 