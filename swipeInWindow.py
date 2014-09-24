#!/usr/bin/python

import sys, time, getopt, os, subprocess
from Quartz.CoreGraphics import * # imports all of the top-level symbols in the module

usageExit = '''%s
Swipe within an OSX window. You must specify relative, not absolute, coordinates. Relative coordinates are < 1 and represent
the percentage of the screen relative to the upper left corner. 

Usage: %s <windowName> <startX> <startY> <endX> <endY> <speed>

Example: %s "iOS Simulator" 0.5 0.5 0.5 0.8 1.2
(drags from middle of the window down to approx. 80 percent of the window, take 1.2 seconds to do the move (default is 0.8))
''' % (sys.argv[0], sys.argv[0], sys.argv[0])

def mouseEvent(type, posx, posy):
    theEvent = CGEventCreateMouseEvent(None, type, (posx,posy), kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, theEvent)
    
def mousemove(posx,posy):
    mouseEvent(kCGEventMouseMoved, posx,posy)
    
def mouseclickdn(posx,posy):
    mouseEvent(kCGEventLeftMouseDown, posx,posy)
    
def mouseclickup(posx,posy):
    mouseEvent(kCGEventLeftMouseUp, posx,posy)
    
def mousedrag(posx,posy):
    mouseEvent(kCGEventLeftMouseDragged, posx,posy)

# Swipe from start coordinate to end coordinate
def swipe(startX, startY, endX, endY, speed):
    print "Swiping from (%d, %d) to (%d, %d)" % (startX, startY, endX, endY)
    ourEvent = CGEventCreate(None) 
    currentpos=CGEventGetLocation(ourEvent) # Save current mouse position
    mouseclickdn(startX, startY)
    time.sleep(speed)
    mousedrag(endX, endY)
    mouseclickup(endX, endY)
    time.sleep(1)
    mousemove(int(currentpos.x),int(currentpos.y)) # Restore mouse position

# Swipe from start to end using relative coordinates (0.5, 0.5) would be middle of screen
# Specify dimensions with sizeX and sizeY
def swipeRelative(startX, startY, endX, endY, sizeX, sizeY, speed):
    # the simulator's "screen" is smaller than the window, which includes the height of the title bar (which says "iOS Simulator")
    # so now we remove height of the title bar
    sizeY = float(sizeY) - 21
    startXOffset = startYOffset = endXOffset = endYOffset = 0

    # the simulator window does not start at (0,0) it is down some (the height of your OSX app bar + the height of the window's title bar (which says "iOS Simulator"))
    # so lets's push everything down a bit
    startYOffset = endYOffset = 43

    # now if we're too close to the edge, bring it back just a tiny bit so that we swipe in the window
    if (endX < 0.01):
        endXOffset = 1
    if (endX > 0.99):
        endXOffset = -1
    if (startX < 0.01):
        startXOffset = 1
    if (startX > 0.99):
        startXOffset = -1

    if (endY < 0.01):
        endYOffset = endYOffset + 1
    if (endY > 0.99):
        endYOffset = endYOffset - 1
    if (startY < 0.01):
        startYOffset = startYOffset + 1
    if (startY > 0.99):
        startYOffset = startYOffset - 1

    x1 = startX * float(sizeX) + startXOffset
    y1 = startY * float(sizeY) + startYOffset
    x2 = endX   * float(sizeX) + endXOffset
    y2 = endY   * float(sizeY) + endYOffset
    swipe (int(x1),int(y1),int(x2),int(y2), speed)
    
# Moves the window to 0,0 so relative coordinates will be accurate
def moveWindowToZero(windowName):
    print "Moving window '%s' to (0,0)" % windowName
    cmd="""
osascript<<END
    tell application "System Events" to tell application process "%s"
    	set position of window 1 to {0, 0}
    end tell
""" % windowName
    os.system(cmd)
    
# Use applescript to bring a window to the foreground
def activateWindow(windowName):
    print "Moving window '%s' to foreground" % windowName
    cmd="""
osascript<<END
    tell application "System Events" to tell application process "%s"
        set frontmost to true 
    end tell
""" % windowName
    os.system(cmd)    

# Use applescript to get the window size
def getWindowSize(windowName):
    cmd="""
osascript<<END
    tell application "System Events" to tell application process "%s"
    	get size of window 1
    end tell
""" % windowName
    dimensions = subprocess.check_output(cmd, shell=True)
    result = dimensions.strip().split(", ")
    print "Window size of '%s' is: %s" % (windowName, result)
    return result  
    
def swipeInWindow(windowName, startX, startY, endX, endY, speed):
    dim = getWindowSize(windowName)
    moveWindowToZero(windowName)
    activateWindow(windowName)
    swipeRelative(startX,startY,endX,endY,dim[0],dim[1], speed)
    
def main():
    #swipeInWindow("iOS Simulator",0.5,0.3,0.5,0.7, 1)

    # Process args
    if (len(sys.argv) < 6):
        print usageExit
        sys.exit(1)

    try:
        speed = float(sys.argv[6])
    except IndexError:
        speed = 0.8
    
    swipeInWindow(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), speed)
    print "Done"

if __name__ == "__main__":
    main()
