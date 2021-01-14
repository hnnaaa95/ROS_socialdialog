#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

from hnna_pkg_test.srv import utterance, utteranceResponse
import rospy
import Inference_test
import re
import random


def handle_add_two_ints(req):
    # y = str("acknowledgement")
    # print("The robot's response expressed as a social cue \n [%s => %s]" % (req.a, y))
    # print("BH's utterance:", req.a)

    # social_cue 추천
    BH_social_cue, BH_sen = Inference_test.input_SC(req.a)
    # print("server1")
    print("Robot's social cue: ", BH_social_cue)

    if BH_social_cue == '9' or BH_social_cue == '1':
        robot_sen = BH_sen
        print("-------대화 종료-------")
        return utteranceResponse(robot_sen)

    else:
        robot_sen = input('counselor sentence : ')
        return utteranceResponse(robot_sen) #chatting version
        #return utteranceResponse(BH_sen) #general version


def add_two_ints_server():
    rospy.init_node('add_two_ints_server')
    s = rospy.Service('add_two_ints', utterance, handle_add_two_ints)
    print("Ready to BH.Lee's utterance.")
    rospy.spin()


if __name__ == "__main__":
    add_two_ints_server()

