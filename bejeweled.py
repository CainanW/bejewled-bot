import os, sys
import Image, ImageGrab, ImageOps
import time, random
from random import randrange
import win32api, win32con
from numpy import *

#Globals
#----------

x_pad = 15
y_pad = 244

game_x_pad = 211 - 15
game_y_pad = 374 - 244

x_space = 40
y_space = 40

color_array_red = zeros((8, 8))
color_array_green = zeros((8, 8))
color_array_blue = zeros((8, 8))

error = 20

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
           # if r > 0 and r < 50 and g > 85 and g < 180 and b > 200 and b < 300:
                #blue
            #    color_array[y,x] = 1
           # elif r > 222 and r < 300 and g > 222 and g < 300 and b > 0 and b < 70:
                #yellow
           #     color_array[y,x] = 2
           # elif r > 170 and r < 222 and g > 50 and g < 100 and b > 0 and b < 50:
                #ornage
            #    color_array[y,x] = 3
           #elif r > 222 and r < 300 and g > 0 and g < 50 and b > 222 and b < 300:
                #purple
            #    color_array[y,x] = 4
           # elif r > 222 and r < 300 and g > 0 and g < 50 and b > 20 and b < 80:
                #red
            #    color_array[y,x] = 5
           # elif r > 0 and r < 50 and g > 100 and g < 180 and b > 0 and b < 50:
                #green
               # color_array[y,x] = 6
           # elif r > 222 and r < 300 and g > 222 and g < 300 and b > 222 and b < 300:
                #white
               # color_array[y,x] = 7
            #else:
                #invalid
                #color_array[y,x] = -1
            #color_array[y,x] = x
            #print(color_array[y,x])


def startPlaying():
    
    
    while (1):
        defineColors()
        #Horizontal Check
        for y in range(8):
            for x in range(7):  
                #if color_array[y][x] == color_array[y][x+1] #and color_array[y][x] > 0:
                if abs(color_array_red[y][x] - color_array_red[y][x+1]) < error:
                    if abs(color_array_green[y][x] - color_array_green[y][x+1]) < error:
                        if abs(color_array_blue[y][x] - color_array_blue[y][x+1]) < error:
                    
                            adjacentHandler(y,x,"horizontal")
        #print("1");
        time.sleep(0.1)
        defineColors()
        #Vertical Check
        for x in range(8):
            for y in range(7):  
                if abs(color_array_red[y+1][x] - color_array_red[y][x]) < error:
                    if abs(color_array_green[y+1][x] - color_array_green[y][x]) < error:
                        if abs(color_array_blue[y+1][x] - color_array_blue[y][x]) < error:
                            adjacentHandler(y,x,"vertical")
        #print("2");
        time.sleep(0.1)
        defineColors()            
        #two spaced half way
        for x in range(8):
            for y in range(8):
                #if x < 6 and color_array[y][x] == color_array[y][x+2] #and color_array[y][x] > 0:
                if x < 6 and abs(color_array_red[y][x] - color_array_red[y][x+2]) < error:
                    if abs(color_array_green[y][x] - color_array_green[y][x+2]) < error:
                        if abs(color_array_blue[y][x] - color_array_blue[y][x+2]) < error:
                            middleHandler(y,x,"horizontal")
                
                #if y < 6 and color_array[y][x] == color_array[y+2][x] #and color_array[y][x] > 0:
                if y < 6 and abs(color_array_red[y][x] - color_array_red[y+2][x]) < error:
                    if abs(color_array_green[y][x] - color_array_green[y+2][x]) < error:
                        if abs(color_array_blue[y][x] - color_array_blue[y+2][x]) < error:
                
                            middleHandler(y,x,"vertical")
        #print("3");        
        time.sleep(0.1)


def adjacentHandler(y,x,direction):

    #y,x gives the value of the top or left most gem

    if direction == "horizontal":
        if x-1 >= 0:
            if y-1 >= 0:
                if sameColor(y,x,y-1,x-1):#color_array[y][x] == color_array[y-1][x-1]:
                    swap(y,x-1,y-1,x-1,y,x,direction,'1')
            if y+1 <= 7:
                if sameColor(y,x,y+1,x-1): #color_array[y][x] == color_array[y+1][x-1]: 
                    swap(y,x-1,y+1,x-1,y,x,direction,'2')
            if x-2 >= 0:
                if sameColor(y,x,y,x-2): #color_array[y][x] == color_array[y][x-2]:
                    swap(y,x-1,y,x-2,y,x,direction,'3')
        
        if x+2 <= 7:
            if y-1 >= 0:
                if sameColor(y,x,y-1,x+2):#color_array[y][x] == color_array[y-1][x+2]:
                    swap(y,x+2,y-1,x+2,y,x,direction,'4')
            if y+1 <= 7:
                if sameColor(y,x,y+1,x+2):#color_array[y][x] == color_array[y+1][x+2]:
                    swap(y,x+2,y+1,x+2,y,x,direction,'5')
            if x+3 <= 7:
                if sameColor(y,x,y,x+3):#color_array[y][x] == color_array[y][x+3]:
                    swap(y,x+2,y,x+3,y,x,direction,'6')

    elif direction == "vertical":
        if y-1 >= 0:
            if x-1 >= 0:
                if sameColor(y,x,y-1,x-1):#color_array[y][x] == color_array[y-1][x-1]:
                    swap(y-1,x,y-1,x-1,y,x,direction,'7')
            if x+1 <= 7:
                if sameColor(y,x,y-1,x+1): #color_array[y][x] == color_array[y-1][x+1]:
                    swap(y-1,x,y-1,x+1,y,x,direction,'8')
            if y-2 >= 0:
                if sameColor(y,x,y-2,x): #color_array[y][x] == color_array[y-2][x]: 
                    swap(y-1,x,y-2,x,y,x,direction,'9')
        
        if y+2 <= 7:
            if x-1 >= 0:
                if sameColor(y,x,y+2,x-1): #color_array[y][x] == color_array[y+2][x-1]: 
                    swap(y+2,x,y+2,x-1,y,x,direction,'10')
            if x+1 <= 7:
                if sameColor(y,x,y+2,x+1): #color_array[y][x] == color_array[y+2][x+1]: 
                    swap(y+2,x,y+2,x+1,y,x,direction,'11')
            if y+3 <= 7:
                if sameColor(y,x,y+3,x): #color_array[y][x] == color_array[y+3][x]: 
                    swap(y+2,x,y+3,x,y,x,direction,'12')
                    
def middleHandler(y,x,direction):

    #y,x gives the value of the top or left most gem

    if direction == "horizontal":
        if y-1 >= 0:

            if sameColor(y,x,y-1,x+1): #color_array[y][x] == color_array[y-1][x+1]: 
                swap(y,x+1,y-1,x+1,y,x,direction,'13')

        if y+1 <= 7:
            if sameColor(y,x,y+1,x+1): #color_array[y][x] == color_array[y+1][x+1]: 
                swap(y,x+1,y+1,x+1,y,x,direction,'14')


    elif direction == "vertical":
        if x-1 >= 0:

            if sameColor(y,x,y+1,x-1): #color_array[y][x] == color_array[y+1][x-1]: 
                swap(y+1,x,y+1,x-1,y,x,direction,'15')

        if x+1 <= 7:
            if sameColor(y,x,y+1,x+1): #color_array[y][x] == color_array[y+1][x+1]: 
                swap(y+1,x,y+1,x+1,y,x,direction,'16')

                

def swap(y1,x1,y2,x2,y,x,direction,number):
    #print ('x: '+str(x)+'y:'+str(y)+'direction'+direction+'number:'+number)
    mousePos((game_x_pad + x1*x_space,game_y_pad + y1*y_space))
    leftDown()

    mousePos((game_x_pad + x2*x_space,game_y_pad + y2*y_space))   
    leftUp()

    #print(str(x1) + ' x ' + str(y1) + ' y ')
    #print('swap with: ' + str(x2) + ' x ' + str(y2) + ' y ')

def sameColor(y1,x1,y2,x2):
    if color_array_red[y1][x1] >= 0 and color_array_red[y2][x2] >= 0:
        if abs(color_array_red[y1][x1] - color_array_red[y2][x2]) < error:
            if abs(color_array_green[y1][x1] - color_array_green[y2][x2]) < error:
                if abs(color_array_blue[y1][x1] - color_array_blue[y2][x2]) < error:
                    return 1
    return 0

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print "Click."          #completely optional. But nice for debugging purposes.

def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    print 'left Down'
         
def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)

def mousePos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))
     
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print x,y

def screenGrab():
    box = (x_pad + 1,y_pad + 1,x_pad + 740,y_pad + 611)
    im = ImageGrab.grab(box)
    ##im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +'.png', 'PNG')
    return im

def everySecond():
    while(1):
        grabWholeScreen()
        time.sleep(5)
    

def grabWholeScreen():
    box = ()
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +'.png', 'PNG')
    return im

def getPixel():
    x_pos,y_pos = win32api.GetCursorPos()
    x_pos = x_pos - x_pad
    y_pos = y_pos - y_pad
    s = screenGrab()
    r, g, b = s.getpixel((x_pos,y_pos))
    print(str(r) + " " + str(g) + " " + str(b))
 
def main():
    screenGrab()
 
if __name__ == '__main__':
    main()
