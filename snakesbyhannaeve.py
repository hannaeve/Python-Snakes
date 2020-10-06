

# Snakes by hannaeve
#
# Player vs. Computer
# Levels 
#       - Easy : The computer has a 10 % chance to get closer to the apple with every movement
#       - Medium : The computer has a 25 % chance to get closer to the apple with every movement
#       - Hard : The computer has a 60 % chance to get closer to the apple with every movement
#       - Extra Hard: The computer a has 100 % chance to get closer to the apple with every movement
#
# The snake with the highest score is the winner
# The game will end if snakes hit each other 

import pyglet, time
from pyglet.window import mouse, key
from pyglet.clock import *
from pyglet.gl import *
import random
glEnable(GL_TEXTURE_2D)

size = 300
add = 70
imgW, imgH = 10, 10
window = pyglet.window.Window(size, size+add)
window.set_caption("Snakes by hannaeve")
batch = pyglet.graphics.Batch()
batch2 = pyglet.graphics.Batch()
img_sprites, sprites, gameplatform = [], [], []

game = {"start": False,
        "level": "medium",
        "difficulty": {
            "easy": 0.10,
            "medium": 0.25,
            "hard": 0.6,
            "extra hard": 1
        },
        "ending": False,
        "directions": {
            key.LEFT: "left",
            key.RIGHT: "right",
            key.UP: "up",
            key.DOWN: "down"
            },
        "levelchoose":{
            key.A: "easy",
            key.B: "medium",
            key.C: "hard",
            key.D: "extra hard"
            },
        "wrongway": {
            "left": "right",
            "right": "left",
            "down": "up",
            "up": "down"},
        "apple": {
                "x": 10,
                "y": 10
                },
        "score":{
            "player": 0,
            "computer": 0
            },
        "winner": ""
        }

graphics = {
    "images": {},
    "background": pyglet.sprite.Sprite(
                        pyglet.image.SolidColorImagePattern((255, 255, 255, 255)).create_image(size, size+add)
                        )
    }

snake = {"player": {"path": [[12,4], [13,4], [14,4]],
                    "information": {
                    "x": 12,
                    "y": 4,
                    "snakeLen": 3,
                    "dir": "",
                    "prevLen": 3
                    }},
         "computer": {"path": [[0,0], [0,1], [0,2]],
                      "information": {
                        "x": 0,
                        "y": 0,
                        "snakeLen": 3,
                        "dir": "up",
                        "prevLen": 3
    }}}

def download_images():
    images={}
    images["player"] = pyglet.resource.image("player.png")
    images["apple"] = pyglet.resource.image("apple.png")
    images["computer"] = pyglet.resource.image("computer.png")
    images["playerSnake"] = pyglet.resource.image("snakeGreen.png")
    images["computerSnake"] = pyglet.resource.image("snakeOrange.png")
    images["0"] = pyglet.resource.image("empty.png")
    images["line"] = pyglet.resource.image("line.png")
    graphics["images"] = images
    
def createGame():
    global gameplatform 
    gameplatform = [["0" for i in range(int(size/imgW))] for j in range(int(size/imgW))]
    for i in range(len(gameplatform)):
        gameplatform[i][len(gameplatform)-1] = "line"  
        
def placeApple():
    size = len(gameplatform)
    freespace = []
    for i in range(1, size-1):
        for j in range(1, size-1):
            if gameplatform[i][j] == "0":
                freespace.append([i,j])

    m = freespace[random.randint(0, len(freespace))]
    game["apple"]["x"] = m[0]
    game["apple"]["y"] = m[1]   
    
def update(dt):
    if game["ending"] == False:
        on_draw()
    else:
        pyglet.clock.unschedule(update)
        
def img_batch():
    for i in range(int(size/imgW)):
        for j in range(int(size/imgH)):
            x, y = i*imgW, j*imgH
            img_sprites.append(pyglet.sprite.Sprite(graphics["images"][gameplatform[i][j]], x, y, batch=batch))
            
def updatePath(snakePar):
    x1 = snakePar["information"]["x"]
    y1 = snakePar["information"]["y"]
    snakePar["path"].append([x1, y1])
    
    if snakePar["information"]["prevLen"] == snakePar["information"]["snakeLen"]:
        gameplatform[snakePar["path"][0][0]][snakePar["path"][0][1]] = "0"
        snakePar["path"].remove(snakePar["path"][0])
    
    snakePar["information"]["prevLen"] = snakePar["information"]["snakeLen"]
    
@window.event
def on_draw():
    window.clear()
    graphics["background"].draw()
    
    if game["start"] == False:
        drawStart()
    else:
        drawGame()
        batch2.draw()
        batch.draw()
        texts()
        if game["ending"] == True:
            draw_text("Game over", int(size/6), size-35, col=(250, 0, 0, 255))
            draw_text("The winner is " + game["winner"].upper() + " ! ", 25, 
                      size-45, size=12, col=(250, 0, 0, 230), bold=True)
            
@window.event
def on_key_press(symbol, modifiers):    
    if game["start"] == False:
        if symbol in [key.A, key.B, key.C, key.D]:
            game["level"] = game["levelchoose"][symbol]
            game["start"] = True
        if symbol == key.E:
            endGame()
    elif game["ending"] == False:
        if symbol in [key.LEFT, key.UP, key.RIGHT, key.DOWN]:
            snake["player"]["information"]["dir"] = game["directions"][symbol]
    
def snakeMoves(snakePar):
    if snakePar["information"]["dir"] == "up":
        snakePar["information"]["y"] += 1
    elif snakePar["information"]["dir"] == "down":
        snakePar["information"]["y"] -= 1
    elif snakePar["information"]["dir"] == "left":
        snakePar["information"]["x"] -= 1
    else:
        snakePar["information"]["x"] += 1
        
    if snakePar["information"]["x"] > len(gameplatform)-1:
        snakePar["information"]["x"] = 0
    elif  snakePar["information"]["x"] < 0:
        snakePar["information"]["x"] = len(gameplatform)-1
    if snakePar["information"]["y"] > len(gameplatform)-2:
        snakePar["information"]["y"] = 0
    elif  snakePar["information"]["y"] < 0:
        snakePar["information"]["y"] = len(gameplatform)-2
        
def computerMoves():
    dirs = ["up", "down", "left", "right"]
    u = random.random()
    
    if u < game["difficulty"][game["level"]]:
        if snake["computer"]["information"]["dir"] == "down" or snake["computer"]["information"]["dir"] == "up":
           if snake["computer"]["information"]["x"] is not game["apple"]["x"]:
                if game["apple"]["x"] < snake["computer"]["information"]["x"]:
                    snake["computer"]["information"]["dir"] = "left"
                else:
                    snake["computer"]["information"]["dir"] = "right"
        else:
            if snake["computer"]["information"]["y"] is not game["apple"]["y"]:
                if game["apple"]["y"] < snake["computer"]["information"]["y"]:
                    snake["computer"]["information"]["dir"] = "down"
                else:
                    snake["computer"]["information"]["dir"] = "up"
    else:
        if u > 0.9:
            dirs.remove(snake["computer"]["information"]["dir"])
            dirs.remove(game["wrongway"][snake["computer"]["information"]["dir"]])
            snake["computer"]["information"]["dir"] = dirs[random.randint(0, len(dirs)-1)]
                
def draw_text(text, x, y, col=(0, 0, 0, 255), font="serif", size=32, bold=False): 
    textbox = pyglet.text.Label(text, 
                      font_name=font,
                      font_size=size,
                      color=col,
                      x=x, y=y,
                      bold=bold,
                      anchor_x="left", anchor_y="bottom")
    textbox.draw()
    
def drawGame():
    if game["ending"] == False:
        snakeMoves(snake["player"])
        
        computerMoves()
        snakeMoves(snake["computer"])
        
        updatePath(snake["player"])
        updatePath(snake["computer"])
        
        if len([elem for elem in snake["player"]["path"] if elem in snake["computer"]["path"]]) > 0:
            game["ending"] = True
            game["winner"] = str([w for w in game["score"] if game["score"][w] == max([game["score"]["player"], 
                                                                                       game["score"]["computer"]])][0])
        
        for x, y in snake["player"]["path"]:
           gameplatform[x][y] = "player" 
         
        for x, y in snake["computer"]["path"]:
           gameplatform[x][y] = "computer" 
        
        gameplatform[game["apple"]["x"]][game["apple"]["y"]] = "apple"
        
        if snake["player"]["information"]["x"] == game["apple"]["x"] and snake["player"]["information"]["y"] == game["apple"]["y"]:
            placeApple()
            snake["player"]["information"]["snakeLen"] += 1
            game["score"]["player"] += 10
        
        if snake["computer"]["information"]["x"] == game["apple"]["x"] and snake["computer"]["information"]["y"] == game["apple"]["y"]:
            placeApple()
            snake["computer"]["information"]["snakeLen"] += 1
            game["score"]["computer"] += 10
        
        img_batch()

def drawStart():
    draw_text("Welcome to play ", 20, 250, size=14, col=(230, 0, 0, 100), bold=True)
    draw_text("snakes by hannaeve", 30, 230, size=14, col=(230, 0, 0, 100), bold=True)
    draw_text("Choose your level", 20, 190, size=12, bold=True)
    draw_text("    Easy (press A)", 20, 170, size=12)
    draw_text("    Medium (press B)", 20, 150, size=12)
    draw_text("    Hard (press C)", 20, 130, size=12)
    draw_text("    Extra Hard (press D)", 20, 110, size=12)
    draw_text("Exit game (press E)", 20, 80, size=12)

def endGame():
    global window
    window.close()
    window = None
    pyglet.app.exit()
    
def texts():
    draw_text("Player  " + str(game["score"]["player"]) + " p", 60, size+35, size=10)
    draw_text("Computer  " + str(game["score"]["computer"]) + " p", 60 , size+10, size=10)
    draw_text("Scores ", 60, size+50, size=12, bold=True)
    draw_text("Level: " + game["level"].upper(), 170, size+35, size=8)

def startGame():
    download_images()
    
    global sprites
    sprites = [pyglet.sprite.Sprite(graphics["images"]["computerSnake"], 20, size+5, batch=batch2), 
               pyglet.sprite.Sprite(graphics["images"]["playerSnake"], 20, size+30, batch=batch2)]
    drawGame()
    drawStart()

    if game["ending"] == False:
        pyglet.clock.schedule_interval(update, 0.2)
        pyglet.app.run()
    
if __name__ == "__main__":
    createGame()
    startGame()


