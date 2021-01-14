#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

from hnna_pkg_test.srv import utterance, utteranceResponse
import rospy

def handle_add_two_ints(req):
    y = str("acknowledgement")
    print("The robot's response expressed as a social cue \n [%s => %s]"%(req.a, y))
    return utteranceResponse(y)

def add_two_ints_server():
    rospy.init_node('add_two_ints_server')
    s = rospy.Service('add_two_ints', utterance, handle_add_two_ints)
    print("Ready to BH.Lee's utterance.")
    rospy.spin()

if __name__ == "__main__":
    add_two_ints_server()
