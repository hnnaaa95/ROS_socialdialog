#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import pickle
import numpy as np
import matplotlib.pyplot as plt
from pomegranate import *
from pomegranate.callbacks import CSVLogger, ModelCheckpoint
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
import pandas as pd
from pandas import DataFrame, Series



class social_dialogue:
    def training_model(self):
        # Load cue data
        with open('/home/kist/catkin_ws/src/hnna_pkg_test/data/dic_visitor_without9', 'rb') as fp:
            dic_visitor_data = pickle.load(fp)
        with open('/home/kist/catkin_ws/src/hnna_pkg_test/data/dic_bao_without9', 'rb') as fp:
            dic_bao_data = pickle.load(fp)
        with open('/home/kist/catkin_ws/src/hnna_pkg_test/data/multi_dic_bao_without9', 'rb') as fp:
            multi_dic_bao_data = pickle.load(fp)

        coder_matching = []
        for i in range(1, 4):
            for j in range(1, 4):
                coder_matching.append((i, j))
        coder_matching = tuple(coder_matching)

        for coder in coder_matching:
            for id in multi_dic_bao_data[coder]:
                j = multi_dic_bao_data[coder][id]
                for n in range(len(j)):
                    if type(j[n]) == int:
                        j[n] = "s" + str(j[n])
                    else:
                        j[n] = list(j[n])
                        for i in range(len(j[n])):
                            j[n][i] = "s" + str(j[n][i])
                        j[n] = tuple(j[n])


        trainset = {}
        testset = {}

        Obs_X =[]
        State_Y =[]

        #코더별로 랜덤 train/test set 나누기 95%:5%
        for coder in coder_matching:
            dic_visitor = dic_visitor_data[coder]
            t_key = random.sample(dic_visitor.keys(),29)
            trainset[coder] = [item for item in list(dic_visitor) if item not in t_key]
            testset[coder] = t_key

        with open('trainset', 'wb') as fp:
            pickle.dump(trainset, fp)
        with open('testset', 'wb') as fp:
            pickle.dump(testset, fp)


        #test/ train set 만들기
        for coder in coder_matching:
            for i in trainset[coder]:
                Obs_X.append(dic_visitor_data[coder][i])
                State_Y.append(dic_bao_data[coder][i])

        for j in State_Y:
            for n in range(len(j)):
                j[n] = "s" + str(j[n])


        x_test = Obs_X
        y_test = State_Y



        # print(method)

        #viterbi 학습 코드
        hmm_model, history = HiddenMarkovModel.from_samples(
            DiscreteDistribution,
            n_components=7,
            X=x_test,
            labels=y_test,
            algorithm='viterbi',
            min_iterations=100, return_history=True, n_jobs=8,
            distribution_inertia=0.45, edge_inertia=0.25, transition_pseudocount=10, emission_pseudocount=10,
            use_pseudocount=True,
            state_names =['s2','s3','s4','s5','s6','s7','s8'],
            callbacks=[CSVLogger('model.logs')]
        )

        #b:emission matrix 저장
        emission =[]
        for s in hmm_model.states:
            try:
                emission.append(s.distribution.parameters)
            except:
                break
        b = []
        for i in range(len(emission)):
            for dic in emission[i]:
                b.append(list(dic.values()))

        #a: transition matrix 저장
        a = hmm_model.dense_transition_matrix()[:-2,:-2]
        b = np.array(b)

        with open('/home/kist/catkin_ws/src/hnna_pkg_test/data/hmm_save_labeled', 'wb') as fp:
            pickle.dump(hmm_model, fp)


        # with open('emission_matrix', 'wb') as fp:
        #     pickle.dump(b, fp)
        # with open('transition_matrix', 'wb') as fp:
        #     pickle.dump(a, fp)


    def predict_hmm(input_cue):
        # print("추론3")

        import rospy
        # print(rospy.get_param('/add_two_ints_server/method'), type(rospy.get_param('/add_two_ints_server/method')))

        if rospy.get_param('/add_two_ints_server/method') == 'v':
            with open('/home/kist/catkin_ws/src/hnna_pkg_test/data/hmm_save_viterbi', 'rb') as fp:
                hmm_model = pickle.load(fp)
        elif rospy.get_param('/add_two_ints_server/method') == 'l':
            with open('/home/kist/catkin_ws/src/hnna_pkg_test/data/hmm_save_labeled', 'rb') as fp:
                hmm_model = pickle.load(fp)
        else:
            print("PLEASE CHOOSE A METHOD")
        #
        # # Load model
        # with open('/home/kist/catkin_ws/src/hnna_pkg_test/data/hmm_save_viterbi','rb') as fp:
        #     hmm_model = pickle.load(fp)
        # with open('/home/kist/catkin_ws/src/hnna_pkg_test/data/hmm_save_labeled','rb') as fp:
        #     hmm_model = pickle.load(fp)

        SC = {'s2': 'self-disclosure elicitation', 's3': 'self-disclosure', 's4': 'suggestion', 's5': 'general statement',
                  's6':'yesno', 's7':'acknowledgement', 's8': 'praise'}

        #model predict
        predict = [state.name for i, state in hmm_model.viterbi(input_cue)[1]][1:]

        # generate sentence
        social_cue_sen = \
            {'None': "없음",
             'Greetings': "안녕하세요",
             's2': random.choice(["그래요?", "진짜요?", "정말요?"]),
             's3': "제가 함부로 말씀드리기 조심스럽네요",
             's4': "000은 어때요?",
             's5': random.choice(["뭐든 꾸준히 하다 보면 좋은 결과가 있기 마련이죠", "세상에 쉬운 일이 없죠"]),
             's6': "네",
             's7': random.choice(["그러시군요", "그랬군요"]),
             's8': random.choice(["힘내세요", "잘했어요", "좋아요"]),
             'Termination': "다음에 또 만나요"}
        #print("병현 :",social_cue_sen[predict[-1]])
        # print("hmm_test")
        return str([SC[i] for i in predict]),social_cue_sen[predict[-1]]





