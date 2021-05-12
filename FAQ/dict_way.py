import pandas as pd
import codecs
import os

def get_synonym_dic():
    FAQ_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    faq_model_dir = os.path.join(FAQ_BASE_DIR, 'data/faq_data')
    entity_file = os.path.join(faq_model_dir, 'question.csv')
    qe_file = os.path.join(faq_model_dir, 'question_keyword.csv')
    syn_file = os.path.join(faq_model_dir,'shangqi_synonym.csv')
    entity_dict = {}
    df_qe = pd.read_csv(qe_file,encoding='gbk')
    df_syn = pd.read_csv(syn_file)
    with codecs.open(entity_file, 'r', 'utf-8') as reader:
        for line in reader.readlines():
            entity_dict[line.strip()] = []
    for index,row in df_qe.iterrows():
        if row['seed_word'] in entity_dict:
            entity_dict[row['seed_word']].append(row['similar_word'].replace(' ',''))

    for index,row in df_syn.iterrows():
        for key in entity_dict:
            if row['seed_word'] in entity_dict[key] and row['similar_word'] not in entity_dict[key]:
                entity_dict[key].append(row['similar_word'])


    return entity_dict

if __name__ == '__main__':
    dict = get_synonym_dic()
    print(dict)
    message = input('此处输入问题')
    answer_dict = {}
    for k in dict:
        for value in dict[k]:
            if value in message:
                if k in answer_dict :
                    if answer_dict[k] < len(value):
                        answer_dict[k] = len(value)
                else:
                    answer_dict[k] = len(value)
    if len(answer_dict) == 0:
        print('没有答案')
    else:
        max = 0
        ans = ''
        for k in answer_dict:
            if len(dict[k]) > max:
                ans = k
    print(answer_dict)
