#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import io
import rospy
from rospy_message_converter import json_message_converter
from rospy_message_converter import message_converter
from std_msgs.msg import String
import json
import pickle

name_strs = '이병현'
# print(dir(name_strs))


def callback(data):
    hnna_dic = json.loads(data.data)
    if hnna_dic['header']['source'] == 'perception':
        if hnna_dic['header']['content'] == ["human_speech"]:            
            if hnna_dic['header']['target'] == ["dialog", "planning"]:
                name = hnna_dic['human_speech']['name']
                name_str = name.encode('utf-8')
           
                if name_str == name_strs:
                    print(name_str)
                    print(hnna_dic["human_speech"]["speech"])
                    print("\n")








def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('recognitionResult', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    name_list = []
    listener()


# #publisher
# import rospy
# from std_msgs.msg import String

# def talker():
#     pub = rospy.Publisher('SocialDialogManager', String, queue_size=10)
#     rospy.init_node('talker', anonymous=True)
#     rate = rospy.Rate(10) # 10hz
#     while not rospy.is_shutdown():
#         hello_str = "hello world %s" % rospy.get_time()
#         rospy.loginfo(hello_str)
#         pub.publish(hello_str)
#         rate.sleep()

# if __name__ == '__main__':
#     try:
#         talker()
#     except rospy.ROSInterruptException:
#         pass
