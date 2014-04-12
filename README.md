swipeInWindow.py
================

A silly little python script that allows swiping within an OSX window using mouse events and Applescript.

It accomplishes this by using Applescript to move the window to position (0,0) and into the foreground. The coordinates to swipe are calculated using the window size. Then it uses python Quartz bindings to send mouse events to those coordinates.

This script can be used to get around the current bug where dragging is broken in Xcode 5.1 + UIAutomation + iOS 7.1 Simulator.

For details on the issue: 

http://stackoverflow.com/questions/18792965/uiautomations-draginsidewithoptions-has-no-effect-on-ios7-simulator

## Requirements

* OSX
* Assistive Devices and Applications enabled
   * OSX 10.9 - System Preferences > Security & Privacy > Privacy > Accessibility > Check "Terminal" and "Accessibility Inspector"
   * OSX 10.8 - System Preferences > Accessibility > Check "Enable access for assistive devices"

## Usage

Swipe within an OSX window. You must specify relative, not absolute, coordinates. Relative coordinates are < 1 and represent
the percentage of the screen relative to the upper left corner.

Usage:

    ./swipeInWindow.py <windowName> <startX> <startY> <endX> <endY>

Example:
(drags from middle of the window down to approx. 80 percent of the window)

    ./swipeInWindow.py "iOS Simulator" 0.5 0.5 0.5 0.8

## Known Issues

* The Y coordinate might be a bit offset due to the OSX title bar
