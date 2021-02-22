# Name: Malcolm
# Date: May 10, 2019
# Title: Frogger
# Features:
# - lives, animation and background music
# - levels (change of speed & number of obstacles), try again function
# Known Issues:
# - Program keeps running after all the homes are reached
# - There are no added game elements(e.g. fly, diving turtle, crocodile log)
# - Program gives an error message after 'window' closes

# Tkinter for GUI
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import threading
import random
import time

# Quit the program
def quitGame():

    window.destroy()

# Moving the frog at the same pace with logs and turtles
def frogJump(direction, jumpStep, dX, dY):

    # Configure the frog image
    canvas.itemconfig(frog, image = frogImageList[direction][jumpStep])

    # If the frog is not moving
    if jumpStep == 0:

        # Move the frog
        canvas.move(frog, dX, dY)

        if canvas.coords(frog)[1] > 100 and canvas.coords(frog)[1] < 350:

            # Frog on top of logs
            log = frogIntersects(logList)

            # Frog on top of turtles
            turtles = frogIntersects(turtlesList)

            # If the frog intersects with a log
            if log:

                # Make the speed of the frog the same as the log it is on
                # ** min function used to get the item handle
                dX = float(canvas.gettags(min(log))[0])

                # Configure the new frog speed
                canvas.itemconfig(frog, tags = (dX))

            # If the frog intersects with a turtle
            elif turtles:

                # Make the speed of the frog the same as the log it is on
                # ** min function used to get the item handle
                dX = float(canvas.gettags(min(turtles))[0])

                # Configure the new frog speed
                canvas.itemconfig(frog, tags = (dX))

            # If the frog intersects with the river
            else:
                gameOver('DROWN')

        # Set the frog speed back to 0 if not on the river section
        elif canvas.gettags(frog)[0] != 0:

            canvas.itemconfig(frog, tags = (0))

# Game over
def gameOver(reason):

##    gameFrame.unbind('<Key>', key)

    if reason != 'CONGRATULATIONS':

        # Stop the frog
        canvas.itemconfig(frog, tags = (0))
        
        # Show its dead image
        canvas.itemconfig(frog, image = frogDeadImage)
        
        # Show message stating the game is over
        tk.messagebox.showwarning(reason, 'Sorry, game over!')
        
        # Ask if the player wants to try again
        tryAgain = tk.messagebox.askyesno('Try Again', 'Would you like to try again?')

        # If so
        if tryAgain == True:

            # Set the original frog image back to its starting position
            frogJump(direction, jumpStep, 0, 0)
            canvas.coords(frog, 400, 675)
            gameFrame.bind('<Key>', key)

        # If not
        else:

            # Return to home screen
            quitGame()

    else:

        ok = tk.messagebox.askyesno(reason, 'You Win!')
        if ok == True:

            gameFrame.place_forget()
            modeFrame.place(x = 0, y = 0)
            modeFrame.focus_set()
#
def frogIntersects(objectList):

    # Create a bounding box for the frog
    bboxFrog = canvas.bbox(frog)

    # Return the intersection set of the frog and the objects in the list
    return set(objectList) & set(canvas.find_overlapping(*bboxFrog))

#
def key(event):

    # If 'w', 'a', 's', or 'd' is pressed
    if event.char == 'w' or event.char == 'd' or event.char == 's' or event.char == 'a':

        # Initialize variables
        direction = 0
        dX = 0
        dY = 0

        # If statements & different variables for each key 
        if event.char == 'w':

            if canvas.coords(frog)[1] > 100:

                direction = 0
                dY = -50

            else:

                gameOver('OUT OF BOUNDS')

        elif event.char == 'd':

            if canvas.coords(frog)[0] < 800:

                direction = 1
                dX = 50

            else:

                gameOver('OUT OF BOUNDS')

        elif event.char == 's':

            if canvas.coords(frog)[1] < 650:

                direction = 2
                dY = 50

            else:

                gameOver('OUT OF BOUNDS')

        elif event.char == 'a':

            if canvas.coords(frog)[0] > 0:

                direction = 3
                dX = -50

            else:

                gameOver('OUT OF BOUNDS')

        # Start timers to get the frog to move through its jump steps
        jumpStep1=threading.Timer(0.05, frogJump, [direction, 1, dX, dY]).start()
        jumpStep2=threading.Timer(0.10, frogJump, [direction, 2, dX, dY]).start()
        jumpStep0=threading.Timer(0.15, frogJump, [direction, 0, dX, dY]).start()

#
def moveObjects():

    # Access global variables
    global speed
    global homeCount

    # Pack the canvas into the game frame
    canvas.pack()

    # Move every object
    for currentObject in moveList:

        dX = float(canvas.gettags(currentObject)[0])

        canvas.move(currentObject, dX, 0)

        # If an object (not the frog) leaves the screen, show it again from the opposite side
        if canvas.coords(currentObject)[0] > 1000:

            canvas.move(currentObject, -1200, 0)

        elif canvas.coords(currentObject)[0] < -200:

            canvas.move(currentObject, 1200, 0)
               
        # Controlling the frog
        if currentObject == frog:

            # If the frog leaves the screen
            if canvas.coords(frog)[0] < 0 or canvas.coords(frog)[0] > 800:

                gameOver('OUT OF BOUNDS')
                
            # If the frog is within the bottom half of the screen
            elif canvas.coords(frog)[1] > 400 and canvas.coords(frog)[1] < 650:

                # If the frog intersects with a vehicle
                if frogIntersects(vehicleList):

                    gameOver('HIT')

            # If the frog is past the river
            elif canvas.coords(frog)[1] < 100:

                home = frogIntersects(homeList)

                # If the frog reaches home
                # **min used to get the item handle
                if home:

                    homeCount += 1

                    # Show the frog's home image
                    canvas.itemconfig(min(home), image = frogHomeImage)
                    canvas.coords(frog, 400, 675)

                    # For every automatically moving object
                    for currentObject in autoMoveList:

                        # If the object is moving to the right, make it faster towards the right
                        if float(canvas.gettags(currentObject)[0]) > 0:
                        
                            canvas.itemconfig(currentObject, tags = float(canvas.gettags(currentObject)[0]) + 0.5)

                        # If the object is moving to the left, make it faster towards the left
                        elif float(canvas.gettags(currentObject)[0]) < 0:

                            canvas.itemconfig(currentObject, tags = float(canvas.gettags(currentObject)[0]) - 0.5)

                    # Player reaches all 5 homes
                    if homeCount == 5:
                        
                        gameOver('CONGRATULATIONS')
                    
                        
                # If the frog does not reach home, it hits the grass
                else:

                    gameOver('GRASS')

    # Start the moveObjects function again
    threading.Timer(0.001, moveObjects).start()

    if homeCount == 5:

        threading.Timer(0.001, moveObjects).cancel()

#
def showGame(level):

    # Access global variables
    global moveList
    global autoMoveList

    # Add images to object lists according to level:
    # Higher levels: more vehicles, less logs & turtles
    # Lower levels: vice versa
    if level == 0:
        logList.append(canvas.create_image(100, 125, image=mediumLogImage, tags = str(speed+2)))
        logList.append(canvas.create_image(0, 275, image=shortLogImage, tags = str(speed+1)))
        turtlesList.append(canvas.create_image(100, 175, image=turtles21Image, tags = ('-' + str(speed+1),'normal')))
        turtlesList.append(canvas.create_image(150, 325, image=turtles31Image, tags = ('-' + str(speed+2),'normal')))

    if level == 0 or level == 1:
        logList.append(canvas.create_image(350, 125, image=mediumLogImage, tags = str(speed+2)))
        logList.append(canvas.create_image(150, 225, image=longLogImage, tags = '-' + str(speed+3)))
        logList.append(canvas.create_image(350, 275, image=shortLogImage, tags = str(speed+1)))
        turtlesList.append(canvas.create_image(300, 175, image=turtles22Image, tags = ('-' + str(speed+1),'normal')))
        turtlesList.append(canvas.create_image(400, 325, image=turtles32Image, tags = ('-' + str(speed+2),'normal')))

    if level == 1 or level == 2:
        vehicleList.append(canvas.create_image(600, 425, image=truckImage, tags = '-' + str(speed)))
        vehicleList.append(canvas.create_image(650, 525, image=purpleCarImage, tags = '-' + str(speed+2)))
        vehicleList.append(canvas.create_image(650, 575, image=dozerImage, tags = str(speed+1)))
        vehicleList.append(canvas.create_image(700, 625, image=yellowCarImage, tags = '-' + str(speed+1)))

    if level == 2:
        vehicleList.append(canvas.create_image(800, 525, image=purpleCarImage, tags = '-' + str(speed+2)))
        vehicleList.append(canvas.create_image(800, 575, image=dozerImage, tags = str(speed+1)))

    # Update global variables
    moveList = vehicleList + logList + turtlesList + [frog]
    autoMoveList = vehicleList + logList + turtlesList

    # Close the mode frame, open the game frame
    modeFrame.place_forget()
    gameFrame.place(x = 0, y = 0)
    # Set the focus on the game frame
    gameFrame.focus_set()
    # Move the objects
    moveObjects()

#
def setupModeFrame():

    # Create frogger label
    froggerLabel = tk.Label(modeFrame, text = 'FROGGER!', anchor = 'center')
    froggerLabel.place(x = 350, y = 200, width = 100, height = 50)

    # Create level buttons
    easyButton = tk.Button(modeFrame, text = 'EASY', command = lambda: showGame(0))
    easyButton.place(x = 200, y = 400, width = 100, height = 50)

    mediumButton = tk.Button(modeFrame, text = 'MEDIUM', command = lambda: showGame(1))
    mediumButton.place(x = 350, y = 400, width = 100, height = 50)

    hardButton = tk.Button(modeFrame, text = 'HARD', command = lambda: showGame(2))
    hardButton.place(x = 500, y = 400, width = 100, height = 50)
            
### Main Program ###
window = tk.Tk()

# Setup the window (800x800)
frameWidth = 800
frameHeight = 800
window.minsize(frameWidth, frameHeight)
window.title('Malcolm and Hanson\'s Frogger')

# Create the game frame and locate it in the top left corner of the window
gameFrame=ttk.Frame(window, width = frameWidth, height = frameHeight, style = 'black.TFrame')
gameFrame.place(x = 0, y = 0)

modeFrame=ttk.Frame(window, width = frameWidth, height = frameHeight)
modeFrame.place(x = 0, y = 0)

# Set the focus on the mode frame
modeFrame.focus_set()

# Bind the keyboard with the key(event) function
gameFrame.bind('<Key>', key)

# Create the canvas, size in pixels (800x800)
canvas = tk.Canvas(gameFrame, width = frameWidth, height = 800)

# Pack the canvas into the frame

# Load the .gif image files - <filename>Image
backgroundImage = tk.PhotoImage(file='images\\background.gif')
dozerImage = tk.PhotoImage(file='images\\dozer.gif')
flyImage = tk.PhotoImage(file='images\\fly.gif')
frogDeadImage = tk.PhotoImage(file='images\\frogDead.gif')
frogHomeImage = tk.PhotoImage(file='images\\frogHome.gif')
greenCarImage = tk.PhotoImage(file='images\\greenCar.gif')
homeImage = tk.PhotoImage(file='images\\home.gif')
longLogImage = tk.PhotoImage(file='images\\longLog.gif')
mediumLogImage = tk.PhotoImage(file='images\\mediumLog.gif')
purpleCarImage = tk.PhotoImage(file='images\\purpleCar.gif')
riverImage = tk.PhotoImage(file='images\\river.gif')
shortLogImage = tk.PhotoImage(file='images\\shortLog.gif')
truckImage = tk.PhotoImage(file='images\\truck.gif')
yellowCarImage = tk.PhotoImage(file='images\\yellowCar.gif')
turtles21Image = tk.PhotoImage(file='images\\turtles21.gif')
turtles22Image = tk.PhotoImage(file='images\\turtles22.gif')
turtles23Image = tk.PhotoImage(file='images\\turtles23.gif')
turtles31Image = tk.PhotoImage(file='images\\turtles31.gif')
turtles32Image = tk.PhotoImage(file='images\\turtles32.gif')
turtles33Image = tk.PhotoImage(file='images\\turtles33.gif')

# Create a list of lists to store all the frog images based on direction and jumpStep
frogImageList = [[],[],[],[]]

for direction in range(4):
    for jumpStep in range(3):
        frogImageList[direction].append(tk.PhotoImage(file='images\\frog' +
                                        str(direction) + str(jumpStep) + '.gif'))

# Create the images on the canvas and create sublists of different object types
canvas.create_image(400, 400, image=backgroundImage)
river = canvas.create_image(400, 225, image=riverImage)

# Set global variables for speed
speed = 1
homeCount = 0

# Create lists of the different types of objects and
# set their initial position, image, direction and speed

# Different number of objects for different levels
vehicleList = []
vehicleList.append(canvas.create_image(200, 425, image=truckImage, tags = '-' + str(speed)))
vehicleList.append(canvas.create_image(400, 475, image=greenCarImage, tags = str(speed+4)))
vehicleList.append(canvas.create_image(150, 525, image=purpleCarImage, tags = '-' + str(speed+2)))
vehicleList.append(canvas.create_image(350, 575, image=dozerImage, tags = str(speed+1)))
vehicleList.append(canvas.create_image(0, 625, image=yellowCarImage, tags = '-' + str(speed+1)))

logList = []
logList.append(canvas.create_image(600, 125, image=mediumLogImage, tags = str(speed+2)))
logList.append(canvas.create_image(550, 225, image=longLogImage, tags = '-' + str(speed+3)))
logList.append(canvas.create_image(700, 275, image=shortLogImage, tags = str(speed+1)))
    
# Turtles have an extra tag to track their type - regular or diving
turtlesList = []
turtlesList.append(canvas.create_image(500, 175, image=turtles23Image, tags = ('-' + str(speed+1),'normal')))
turtlesList.append(canvas.create_image(700, 175, image=turtles21Image, tags = ('-' + str(speed+1),'normal')))
turtlesList.append(canvas.create_image(650, 325, image=turtles33Image, tags = ('-' + str(speed+2),'normal')))

homeList = []
homeList.append(canvas.create_image(100, 75, image=homeImage, tags = '0'))
homeList.append(canvas.create_image(250, 75, image=homeImage, tags = '0'))
homeList.append(canvas.create_image(400, 75, image=homeImage, tags = '0'))
homeList.append(canvas.create_image(550, 75, image=homeImage, tags = '0'))
homeList.append(canvas.create_image(700, 75, image=homeImage, tags = '0'))

# Create the frog and set its initial position, image (sitting up) and direction and speed to 0
frog = canvas.create_image(400, 675, image=frogImageList[0][0], tags = '0')

# Create a list of all the movable objects
moveList = vehicleList + logList + turtlesList + [frog]
autoMoveList = vehicleList + logList + turtlesList

# Setup the first frame
setupModeFrame()

# Start the program
window.mainloop()
                   
                   

            

