#---------- BEJEWELED BOT ----------
# This bot was oroginally created to beat my friend at bejeweled blitz.
# You may have to configure the game_x_pad and game_y_pad so that the bot clicks in the right area.

import os, sys
import Image, ImageGrab, ImageOps
import time, random
from random import randrange
import win32api, win32con
from numpy import *

#Globals
#----------

#x_pad and y_pad indicate the the offset of the screen to the game area (Change depending on where window is)
x_pad = 8
y_pad = 277

#game_x_pad and game_y_pad indicate the the offset start of game screen to the bejeweled board (DONT CHANGE)
game_x_pad = 203 - x_pad
game_y_pad = 406 - y_pad

x_space = 40
y_space = 40

color_array_red = zeros((8, 8))
color_array_green = zeros((8, 8))
color_array_blue = zeros((8, 8))

error = 20

#End Globals
#----------

# Gets the color of each gem in the 8x8 matrix
def defineColors():
    s = screenGrab()
    for x in range(8):
        for y in range(8):
            #time.sleep(0.1);
            r, g, b = s.getpixel((game_x_pad + x*x_space,game_y_pad + y*y_space))
            #mousePos((game_x_pad + x*x_space,game_y_pad + y*y_space))
            #print(str(x) + " " + str(y) + ": " + str(r) + " " + str(g) + " " + str(b) + " ")
            color_array_red[y,x] = r
            color_array_green[y,x] = g
            color_array_blue[y,x] = b

            if(r<100 and g<100 and b<100):
                color_array_red[y,x] = -1
                color_array_green[y,x] = -1
                color_array_blue[y,x] = -1

# 'Main' Method
def startPlaying():
    
    start_Time = time.time()
    while (1):
        #Get Gem colors
        defineColors()
        #Check for two Gems of the same color Horizontally aligned
        for y in range(8):
            for x in range(7):  
                if abs(color_array_red[y][x] - color_array_red[y][x+1]) < error:
                    if abs(color_array_green[y][x] - color_array_green[y][x+1]) < error:
                        if abs(color_array_blue[y][x] - color_array_blue[y][x+1]) < error:
                    
                            adjacentHandler(y,x,"horizontal")
        time.sleep(0.1)
        defineColors()
        #Check for two Gems of the same color Vertically aligned
        for x in range(8):
            for y in range(7):  
                if abs(color_array_red[y+1][x] - color_array_red[y][x]) < error:
                    if abs(color_array_green[y+1][x] - color_array_green[y][x]) < error:
                        if abs(color_array_blue[y+1][x] - color_array_blue[y][x]) < error:
                            adjacentHandler(y,x,"vertical")
        time.sleep(0.1)
        defineColors()            
        #Check for two Gems of the same color separated by one gem
        for x in range(8):
            for y in range(8):
                if x < 6 and abs(color_array_red[y][x] - color_array_red[y][x+2]) < error:
                    if abs(color_array_green[y][x] - color_array_green[y][x+2]) < error:
                        if abs(color_array_blue[y][x] - color_array_blue[y][x+2]) < error:
                            middleHandler(y,x,"horizontal")
                
                if y < 6 and abs(color_array_red[y][x] - color_array_red[y+2][x]) < error:
                    if abs(color_array_green[y][x] - color_array_green[y+2][x]) < error:
                        if abs(color_array_blue[y][x] - color_array_blue[y+2][x]) < error:
                
                            middleHandler(y,x,"vertical")      
        time.sleep(0.1)

        #If we have run for 60 seconds, stop the program (games are only 60 seconds long)
        if(time.time() - start_Time > 60):
            break
        

#Checks adjacent same-colored gems for a possible 3rd gem to swap with and get 3 in a row.
#y,x gives the value of the top or left most gem
def adjacentHandler(y,x,direction):

    if direction == "horizontal":
        if x-1 >= 0:
            if y-1 >= 0:
                if sameColor(y,x,y-1,x-1):
                    swap(y,x-1,y-1,x-1,y,x,direction,'1')
            if y+1 <= 7:
                if sameColor(y,x,y+1,x-1): 
                    swap(y,x-1,y+1,x-1,y,x,direction,'2')
            if x-2 >= 0:
                if sameColor(y,x,y,x-2): 
                    swap(y,x-1,y,x-2,y,x,direction,'3')
        
        if x+2 <= 7:
            if y-1 >= 0:
                if sameColor(y,x,y-1,x+2):
                    swap(y,x+2,y-1,x+2,y,x,direction,'4')
            if y+1 <= 7:
                if sameColor(y,x,y+1,x+2):
                    swap(y,x+2,y+1,x+2,y,x,direction,'5')
            if x+3 <= 7:
                if sameColor(y,x,y,x+3):
                    swap(y,x+2,y,x+3,y,x,direction,'6')

    elif direction == "vertical":
        if y-1 >= 0:
            if x-1 >= 0:
                if sameColor(y,x,y-1,x-1):
                    swap(y-1,x,y-1,x-1,y,x,direction,'7')
            if x+1 <= 7:
                if sameColor(y,x,y-1,x+1): 
                    swap(y-1,x,y-1,x+1,y,x,direction,'8')
            if y-2 >= 0:
                if sameColor(y,x,y-2,x): 
                    swap(y-1,x,y-2,x,y,x,direction,'9')
        
        if y+2 <= 7:
            if x-1 >= 0:
                if sameColor(y,x,y+2,x-1): 
                    swap(y+2,x,y+2,x-1,y,x,direction,'10')
            if x+1 <= 7:
                if sameColor(y,x,y+2,x+1): 
                    swap(y+2,x,y+2,x+1,y,x,direction,'11')
            if y+3 <= 7:
                if sameColor(y,x,y+3,x): 
                    swap(y+2,x,y+3,x,y,x,direction,'12')

#Checks two same-colored gems with a different gem in the middle for a possible middle swap                   
def middleHandler(y,x,direction):

    #y,x gives the value of the top or left most gem

    if direction == "horizontal":
        if y-1 >= 0:

            if sameColor(y,x,y-1,x+1): 
                swap(y,x+1,y-1,x+1,y,x,direction,'13')

        if y+1 <= 7:
            if sameColor(y,x,y+1,x+1): 
                swap(y,x+1,y+1,x+1,y,x,direction,'14')


    elif direction == "vertical":
        if x-1 >= 0:

            if sameColor(y,x,y+1,x-1): 
                swap(y+1,x,y+1,x-1,y,x,direction,'15')

        if x+1 <= 7:
            if sameColor(y,x,y+1,x+1): 
                swap(y+1,x,y+1,x+1,y,x,direction,'16')

                
#Swaps two sets of gems with (x,y) co-ords (x1,y1),(x2,y2). x,y,direction and number are for debugging
def swap(y1,x1,y2,x2,y,x,direction,number):
    #print ('x: '+str(x)+'y:'+str(y)+'direction'+direction+'number:'+number)
    mousePos((game_x_pad + x1*x_space,game_y_pad + y1*y_space))
    leftDown()

    mousePos((game_x_pad + x2*x_space,game_y_pad + y2*y_space))   
    leftUp()

    #print(str(x1) + ' x ' + str(y1) + ' y ')
    #print('swap with: ' + str(x2) + ' x ' + str(y2) + ' y ')

#Checks if the gems with (x,y) co-ords (x1,y1),(x2,y2) have the same color
def sameColor(y1,x1,y2,x2):
    if color_array_red[y1][x1] >= 0 and color_array_red[y2][x2] >= 0:
        if abs(color_array_red[y1][x1] - color_array_red[y2][x2]) < error:
            if abs(color_array_green[y1][x1] - color_array_green[y2][x2]) < error:
                if abs(color_array_blue[y1][x1] - color_array_blue[y2][x2]) < error:
                    return 1
    return 0

#Set of commands to allow easy clicking, mouse positioning, and pixel color tracking
#-------

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print "Click." #completely optional. But nice for debugging purposes.          

def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    print 'left Down' #completely optional. But nice for debugging purposes. 
         
def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)

def mousePos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))

#Returns mouse co-ordinates     
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print x,y  #completely optional. But nice for debugging purposes. 

#Grabs screen and returns image
def screenGrab():
    box = (x_pad + 1,y_pad + 1,x_pad + 740,y_pad + 611)
    im = ImageGrab.grab(box)
    ##im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +'.png', 'PNG')
    return im

##Screen Reading Debugging Functions

##def everySecond():
##    while(1):
##        grabWholeScreen()
##        time.sleep(5)
##    
##
##def grabWholeScreen():
##    box = ()
##    im = ImageGrab.grab(box)
##    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +'.png', 'PNG')
##    return im

#Debug function, prtins pixel RGB values at cursor
def getPixel():
    x_pos,y_pos = win32api.GetCursorPos()
    x_pos = x_pos - x_pad
    y_pos = y_pos - y_pad
    s = screenGrab()
    r, g, b = s.getpixel((x_pos,y_pos))
    print(str(r) + " " + str(g) + " " + str(b))

#-------
 
def main():
    screenGrab()
 
if __name__ == '__main__':
    main()
