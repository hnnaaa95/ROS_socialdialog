import social_classifier
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


#


clf = social_classifier.Social_classifier()

import hmm_test2
input_cue = []
hmm_test2.social_dialogue.training_model

# 추론 문장 입력
while (1):
    input_sentence = input("Human Input sentence : ")

    # classification
    print("Human's social cue: ",social_cue[clf.infer(input_sentence)])
    if clf.infer(input_sentence) == 9 or clf.infer(input_sentence) == 1:
        break
    else:
        input_cue.append(clf.infer(input_sentence))
        hmm_test2.social_dialogue.predict_hmm(input_cue)



