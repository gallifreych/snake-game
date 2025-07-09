import tkinter
import random
import time

ROWS = 25
COLS = 25
KARE = 25

WINDOW_WIDTH = KARE * ROWS
WINDOW_HEIGHT = KARE * COLS

class Tile:
    def __init__(self, x, y):
        self.x =x
        self.y =y

window = tkinter.Tk()
window.title("Yılan Oyunu")
window.resizable(False,False)

canvas = tkinter.Canvas(window, bg= "DarkGreen", width= WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)

canvas.pack()
window.update()

PENCERE_WIDTH = window.winfo_width()
PENCERE_HEIGHT = window.winfo_height()
EKRAN_WIDTH = window.winfo_screenwidth()
EKRAN_HEIGHT = window.winfo_screenheight()

window_x = int((EKRAN_WIDTH/2) - (PENCERE_WIDTH/2))
window_y = int((EKRAN_HEIGHT/2) - (PENCERE_HEIGHT/2))

#pencereyi ekranın ortasında aç
#formül= width x height + x + y.
window.geometry(f"{PENCERE_WIDTH}x{PENCERE_HEIGHT}+{window_x}+{window_y}")

#yılanı ve yemeği şu karede başlat
snake= Tile(10*KARE,10*KARE) 
food = Tile(15*KARE,10*KARE)
snake_body = []
velocityX = 0
velocityY = 0
gameOver = False
puan = 0

def change_direction(e):
   global velocityX, velocityY, gameOver
   if(e.keysym== "Up" and velocityY !=1):
    velocityX= 0
    velocityY= -1
   elif(e.keysym == "Down" and velocityY != -1):
    velocityX = 0
    velocityY = 1
   elif(e.keysym == "Left" and velocityX != 1):
    velocityX = -1
    velocityY = 0
   elif(e.keysym == "Right" and velocityX != -1):
    velocityX = 1
    velocityY = 0
    if(gameOver):
       return
    
def move():
    global snake ,food, snake_body, gameOver, puan
    if(gameOver):
       return
    #kenarlara veya kendine çarparsa game over
    if(snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >=WINDOW_HEIGHT):
           gameOver = True
           return
    
    for tile in snake_body:
       if(snake.x == tile.x and snake.y == tile.y):
          gameOver = True
          return

    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0,COLS-1) * KARE
        food.y = random.randint(0,ROWS-1) * KARE
        puan += 1 
    for i in range(len(snake_body)-1, -1, -1):
       tile = snake_body[i]
       if(i == 0):
           tile.x = snake.x
           tile.y = snake.y
       else:
           prev_tile = snake_body[i-1]
           tile.x = prev_tile.x
           tile.y = prev_tile.y

        
    snake.x += velocityX * KARE
    snake.y += velocityY * KARE
  
def restart_game():
    global snake, food, snake_body, velocityX, velocityY, gameOver, puan

    snake = Tile(10 * KARE, 10 * KARE)
    food = Tile(15 * KARE, 10 * KARE)
    snake_body = []
    velocityX = 0
    velocityY = 0
    gameOver = False
    puan = 0

def handle_key(er):
    if er.keysym == "r" or er.keysym == "R":
        if gameOver:
            restart_game()
    else:
        change_direction(er)
def draw():
    global snake, food, snake_body, gameOver, puan
    move()
    canvas.delete("all")
    #yem
    canvas.create_rectangle(food.x, food.y, food.x+KARE, food.y+KARE, fill="red")
    #yılan
    canvas.create_rectangle(snake.x, snake.y, snake.x+KARE, snake.y+KARE, fill="white")
    
    for tile in snake_body:
       canvas.create_rectangle(tile.x, tile.y, tile.x+KARE, tile.y+KARE, fill="lime")

    if(gameOver):
       canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Tahoma 50 bold", text = f"Oyun Bitti", fill="Red")
       canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 45, font="Arial 20", text = f"Puan:{puan}", fill="white")
       canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 150,
                   font="Arial 10", text="Tekrar Oynamak İçin R Tuşuna Basın.", fill="white")
    else:
       canvas.create_text(30,20, font="TimesNewRoman 15", text = f"Puan:{puan}", fill="white" )        
    #0.1 saniye sonra tekrar çiz (sürekli çizer)
    window.after(100,draw) 
draw()

window.bind("<KeyRelease>", handle_key)
window.mainloop()