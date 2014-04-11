swipeInWindow.py
================

A silly little python script that will allows swiping within an OSX window using mouse events and Applescript. 
This can be used to get around the current bug with Xcode 5.1 + iOS 7.1 simulators where swiping is broken.
See: http://stackoverflow.com/questions/18792965/uiautomations-draginsidewithoptions-has-no-effect-on-ios7-simulator

Usage
=====

Swipe within an OSX window. You must specify relative, not absolute coordinates. 

Usage: ./swipeInWindow.py <windowName> <startX> <startY> <endX> <endY> 

Example: ./swipeInWindow.py "iOS Simulator" 0.5 0.5 0.5 0.8 
(drags from middle of the window down to approx. 80 percent of the window)

