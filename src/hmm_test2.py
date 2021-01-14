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
        with open('/home/kist/repository/deeptask_woz_tagger/expaded_data/dic_visitor_without9', 'rb') as fp:
            dic_visitor_data = pickle.load(fp)
        with open('/home/kist/repository/deeptask_woz_tagger/expaded_data/dic_bao_without9', 'rb') as fp:
            dic_bao_data = pickle.load(fp)
        with open('/home/kist/repository/deeptask_woz_tagger/expaded_data/multi_dic_bao_without9', 'rb') as fp:
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

        with open('/home/kist/repository/deeptask_woz_tagger/expaded_data//hmm_save', 'wb') as fp:
            pickle.dump(hmm_model, fp)


        # with open('emission_matrix', 'wb') as fp:
        #     pickle.dump(b, fp)
        # with open('transition_matrix', 'wb') as fp:
        #     pickle.dump(a, fp)


    def predict_hmm(input_cue):

        #시험삼아
            



        # Load model
        with open('/home/kist/repository/deeptask_woz_tagger/expaded_data//hmm_save','rb') as fp:
            hmm_model = pickle.load(fp)

        SC = {'s2': 'self-disclosure elicitation', 's3': 'self-disclosure', 's4': 'suggestion', 's5': 'general statement',
                  's6':'yesno', 's7':'acknowledgement', 's8': 'praise'}

        #model predict
        predict = [state.name for i, state in hmm_model.viterbi(input_cue)[1]][1:]

        return print("robot's social cue: ",[SC[i] for i in predict],"\n")





