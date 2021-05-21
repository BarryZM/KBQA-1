
#访问rasa的API接口的专用函数
import json
import secrets

import requests


def post(url, data=None):
    data = json.dumps(data, ensure_ascii=False)
    data = data.encode(encoding="utf-8")
    r = requests.post(url=url, data=data)
    # print(r)
    r = json.loads(r.text)
    return r

# url = "http://localhost:5005/webhooks/rest/webhook"
url = "http://47.100.22.16:5005/webhooks/rest/webhook"
sender = secrets.token_urlsafe(16)

def main():
    while True:
        message = input("Your input ->  ")
        if message == 'exit':
            break
        data = {"sender": sender, "message": message}
        resp = post(url=url,data=data)
        # print('resp',resp)
        for i in resp:
            print('resp', i)

if __name__ == '__main__':
    main()



'''
提问：G20多少钱
[{'intent': 'KBQA'},
{'action': 'action_kbqa'},
{'slots': 
    {'car_series': '旅行家G20','attribute': ['市场指导价'],
    'car_model': None,'object_type': None,
    'listed_items': None,'mention': None,
    'mood': None,'last_actions_name': None,
     'last_intent_name': None, 'car_skill': None,
      'last_turn_car_skill': None, 'replay_type': None}
},
{'recipient_id': '0oY5ArBTRJdj3tyjBCaTPA', 'text': '小通为您查询到如下结果:'},
{'recipient_id': '0oY5ArBTRJdj3tyjBCaTPA', 'text': "2021款 时光版: {'市场指导价': '309800'}"},
{'recipient_id': '0oY5ArBTRJdj3tyjBCaTPA', 'text': "2021款 阳光版: {'市场指导价': '269800'}"}]

提问：阅读灯怎么使用
[{'intent': 'FAQ'},
{'action': 'action_faq'},
{'slots': 
    {'car_series': '旅行家G20', 'attribute': None,
    'car_model': None, 'object_type': None,
    'listed_items': None, 'mention': None,
    'mood': None, 'last_actions_name': None,
    'last_intent_name': None, 'car_skill': None,
    'last_turn_car_skill': None, 'replay_type': None}
},
{'recipient_id': '0oY5ArBTRJdj3tyjBCaTPA', 'text': '由阅读灯底座中间的触摸开关控制。'}]


[{'intent': 'FAQ'}, {'action': 'action_faq'},
{'slots': 
    {'car_series': '旅行家G20', 'attribute': None, 'car_model': None,
    'object_type': None, 'listed_items': None, 'mention': None,
    'mood': None, 'last_actions_name': None, 'last_intent_name': None,
    'car_skill': None, 'last_turn_car_skill': None, 'replay_type': None}
}, 
{'recipient_id': '0oY5ArBTRJdj3tyjBCaTPA', 'text': '1.必须上拉冰箱门锁后才能将冰箱门外旋打开。2.冰箱内温度有机械旋钮调节。'},
{'recipient_id': '0oY5ArBTRJdj3tyjBCaTPA', 'image': 'faq_imgs/2.jpg'},
{'recipient_id': '0oY5ArBTRJdj3tyjBCaTPA', 'image': 'faq_imgs/3.jpg'}]


{'text': '阅读灯怎么使用',
'intent': {'name': 'FAQ', 'confidence': 0.8289339517084233},
'entities': [],
'intent_ranking':
    [{'name': 'FAQ', 'confidence': 0.8289339517084233},{'name': 'KBQA', 'confidence': 0.049283005853029686},
    {'name': 'car_control', 'confidence': 0.023514298597787236}, {'name': 'out_of_scope', 'confidence': 0.023393420284426866},
    {'name': 'bot_challenge', 'confidence':0.020703864231757664}, {'name': 'goodbye', 'confidence': 0.015981022753539333},
    {'name': 'deny', 'confidence': 0.0140236353406657}, {'name': 'greet', 'confidence': 0.013670050349102299},
    {'name': 'affirm', 'confidence': 0.005298309682802651}, {'name': 'mention_entity', 'confidence': 0.005198441198465226}
    ],
'response_selector': 
    {'all_retrieval_intents': ['KBQA'],
    'KBQA': {
        'response': 
            {'id': -4448462213886833473, 'response_templates': [{'text': '{answer}'}], 'confidence': 0.9853773713111877, 'intent_response_key': 'KBQA/vehicle_information', 'template_name': 'utter_KBQA/vehicle_information'},
            'ranking': [{'id': -4448462213886833473, 'confidence': 0.9853773713111877, 'intent_response_key': 'KBQA/vehicle_iformation'}, {'id': -901383248419734488, 'confidence': 0.014622578397393227, 'intent_response_key': 'KBQA/enterprise_information'}]}}}

输入：INDEL冰箱怎么使用
返回：
    [
    {'intent': 
        [{'name': 'FAQ', 'confidence': 0.8816494872698822},{'name': 'KBQA', 'confidence': 0.04355593594759767},
        {'name': 'out_of_scope', 'confidence': 0.017761032474994522}, {'name': 'bot_challenge', 'confidence': 0.013287137704721275},
        {'name': 'car_control', 'confidence': 0.011470180715142393}, {'name': 'goodbye', 'confidence': 0.00863593429677485},
        {'name': 'greet', 'confidence': 0.008103059493351532}, {'name': 'deny', 'confidence': 0.008009370933762933},
        {'name': 'mention_entity', 'confidence': 0.0040682568113580096}, {'name': 'affirm', 'confidence': 0.003459604352414506}]},
    {'action': 'action_faq'},
    {'slots': 
        {'car_series': None, 'attribute': None, 'car_model': None, 'object_type': None,
        'listed_items': None, 'mention': None, 'mood': None, 'last_actions_name': None,
        'last_intent_name': None, 'car_skill': None, 'last_turn_car_skill': None, 'replay_type': None}},
    {'recipient_id': '0oY5ArBTRJdj3tyjBCaTPA', 'text': '1.必须上拉冰箱门锁后才能将冰箱门外旋打开。2.冰箱内温度有机械旋钮调节。'},
    {'recipient_id': '0oY5ArBTRJdj3tyjBCaTPA', 'image': 'faq_imgs/2.jpg'},
    {'recipient_id': '0oY5ArBTRJdj3tyjBCaTPA', 'image': 'faq_imgs/3.jpg'}
    ]

输入：G20多少钱
返回：
    [
    {'intent': [{'name': 'KBQA', 'confidence': 0.7651076858665014}, {'name': 'FAQ', 'confidence': 0.04657195392271782},
    {'name': 'out_of_scope', 'confidence': 0.03954956615556967}, {'name': 'bot_challenge', 'confidence': 0.030154407675866534},
    {'name': 'goodbye', 'confidence': 0.029448686735691336}, {'name': 'deny', 'confidence': 0.025041248497075824},
    {'name': 'car_control', 'confidence': 0.02026067935754481}, {'name': 'greet', 'confidence': 0.01767381953709061},
    {'name': 'affirm', 'confidence': 0.014596253680488709}, {'name': 'mention_entity', 'confidence': 0.011595698571453686}]},
    {'action': 'action_kbqa'},
    {'slots': 
        {'car_series': '旅行家G20', 'attribute': ['市场指导价'], 'car_model': None, 'object_type': None, 'listed_items': None,
        'mention': None, 'mood': None, 'last_actions_name': None, 'last_intent_name': None, 'car_skill': None,
        'last_turn_car_skill': None, 'replay_type': None}},
    {'recipient_id': '0oY5ArBTRJdj3tyjBCaTPA', 'text': '小通为您查询到如下结果:'},
    {'recipient_id': '0oY5ArBTRJdj3tyjBCaTPA', 'text': "2021款 时光版: {'市场指导价': '309800'}"},
    {'recipient_id': '0oY5ArBTRJdj3tyjBCaTPA', 'text': "2021款 阳光版: {'市场指导价': '269800'}"}
    ]
'''