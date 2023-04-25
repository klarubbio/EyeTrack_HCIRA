"""
Code used by Karina LaRubbio for Human-Centered Input Recognition Algorithms at the University of Florida.
From original repositories by antoinelame and ritko on Github.
Utilizes OpenCV library: https://opencv.org/, among others.
"""

import sys


def get_screensize():
    try:
        if sys.platform in ['Windows', 'win32', 'cygwin']:
            from win32api import GetSystemMetrics
            import win32con
            width_px = GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height_px = GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            return {'width': int(width_px), 'height': int(height_px)}
        elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
            from AppKit import NSScreen
            screen = NSScreen.screens()[0]
            width_px = screen.frame().size.width
            height_px = screen.frame().size.height
            return {'width': int(width_px), 'height': int(height_px)}
        elif sys.platform in ['linux', 'linux2']:
            import Xlib.display
            resolution = Xlib.display.Display().screen().root.get_geometry()
            width_px = resolution.width
            height_px = resolution.height
            return {'width': int(width_px), 'height': int(height_px)}
    except NotImplementedError:
        sys.exit("Platform not recognized. Supported platforms are Windows, MacOS, Linux")
