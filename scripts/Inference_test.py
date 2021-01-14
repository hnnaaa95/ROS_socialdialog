#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#socialcue 분류 모듈
import social_classifier
# import os, sys
# print("파일 이름1",os.path.abspath( __file__ ))

#hmm 실행 모듈
import hmm_test2


social_cue =  {0:'None',
               1:'Greetings' ,
               2:'Self-disclosure eliciation' ,
               3:'Self-disclosure' ,
               4:'Suggestion',
               5:'General Statement',
               6:'Simple yes/no',
               7:'Acknowledgement',
               8:'Praise',
               9:'Termination'}

clf = social_classifier.Social_classifier()

'''
hmm_test2.social_dialogue.training_model
# print("추론1")
'''

import hmm_test2
# train = hmm_test2.social_dialogue()
# train.training_model()
# print("Inference_test path:",sys.path)
# print("파일 이름2",os.path.abspath( __file__ ))

# 추론 문장 입력
input_cue = []
def input_SC(input_sentence):
    # print("추론2")
    print("input_sentence: ", input_sentence)
    print("Human's social cue: ", social_cue[clf.infer(input_sentence)])
    if clf.infer(input_sentence) == 9 or clf.infer(input_sentence) == 1:
        BH_sen = "안녕히 가세요"
        return str(clf.infer(input_sentence)), BH_sen
        # print("Please say again except for the greeting and termination.")
        # exit()
    else:
        input_cue.append(clf.infer(input_sentence))
        return hmm_test2.social_dialogue.predict_hmm(input_cue)







