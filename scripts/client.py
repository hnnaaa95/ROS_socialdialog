#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import rospy
from hnna_pkg_test.srv import *

def add_two_ints_client(x):
    rospy.wait_for_service('add_two_ints')
    try:
        add_two_ints = rospy.ServiceProxy('add_two_ints', utterance)
        resp1 = add_two_ints(x)
        # print("what's this", resp1)
        return resp1.cue

    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    print("counselor : 안녕하세요. 오늘 기분은 어떠세요?")
    return "Please reply using this form -> rosrun hnna_pkg_test client.py [string]"

if __name__ == "__main__":

    if len(sys.argv) == 2:
        x = sys.argv[1]

    else:
        print(usage())
        sys.exit(1)

    # print("The robot's response expressed as a social cue [%s => %s]" % (x, add_two_ints_client(x)))

    # 받아와야할 social cue
    robot_sen = add_two_ints_client(x)
    if robot_sen == "안녕히 가세요":
        print("The robot's response expressed as a social cue [%s => %s]" % (x, robot_sen))
        print("-------대화 종료-------")
        sys.exit(1)
    else:
        print("The robot's response expressed as a social cue [%s => %s]" % (x, robot_sen))
