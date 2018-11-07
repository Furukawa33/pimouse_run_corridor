#!/usr/bin/env python
import rospy

from getch import getch, pause

while True:
    key = ord(getch())
    print(key)
    if key == 13:
        print ("Enter")
        break
#    else:
#        print("You pressed:%s(%d)")

pause()
