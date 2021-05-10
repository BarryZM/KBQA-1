import secrets

from rasa.core.agent import Agent
from rasa.utils.endpoints import EndpointConfig
import asyncio

model_path = 'models/20210505-202031.tar.gz'
endpoint = EndpointConfig(url="http://localhost:5055/webhook")

sender = secrets.token_urlsafe(16)


def main():
    agent = Agent.load(model_path, action_endpoint=endpoint)
    with open('./log.txt', 'w', encoding='utf-8') as f:
        while True:
            message = input("Your input ->  ")
            if message == 'exit':
                break
            # response = asyncio.run(agent.handle_text(message))
            response = asyncio.get_event_loop().run_until_complete(agent.handle_text(message))

            f.write(message)
            f.write('\n')
            f.write(str(response))
            f.write('\n')

            print('resp',response)


if __name__ == '__main__':
    main()

'''
输入：你好
返回：
[
    {'intent': 
        [{'name': 'greet', 'confidence': 0.6961625425168885}, {'name': 'out_of_scope', 'confidence': 0.06439974950216834},
        {'name': 'affirm', 'confidence': 0.06199557255191751},{'name': 'bot_challenge', 'confidence': 0.04617805163570428},
        {'name': 'car_control', 'confidence': 0.03936807305796786}, {'name': 'goodbye', 'confidence': 0.03664971578381771},
        {'name': 'deny', 'confidence': 0.01832237795747234}, {'name': 'KBQA', 'confidence': 0.012701376170215316},
        {'name': 'FAQ', 'confidence': 0.01246439764253417},{'name': 'mention_entity', 'confidence': 0.011758143181314094}]},
    {'action': 'utter_greet'},
    {'slots': 
        {'car_series': None, 'attribute': None, 'car_model': None, 'object_type': None, 'listed_items': None, 'mention': None,
        'mood': None, 'last_actions_name': None, 'last_intent_name': None, 'car_skill': None, 'last_turn_car_skill': None, 'replay_type': None}},
    {'recipient_id': 'default', 'text': '您好有什么为您服务的吗？'}
]
输入：G20多少钱？
返回：
[
    {'intent': 
        [{'name': 'KBQA', 'confidence': 0.45732096904847036}, {'name': 'out_of_scope', 'confidence': 0.13182715617810878}, {'name': 'bot_challenge', 'confidence': 0.1167826797705559},
        {'name': 'deny', 'confidence': 0.07651662570949924}, {'name': 'affirm', 'confidence': 0.06254513426937211}, {'name': 'goodbye', 'confidence': 0.056150153974958324},
        {'name': 'car_control', 'confidence': 0.03996157025648306}, {'name': 'FAQ', 'confidence': 0.030277274911002742}, {'name': 'greet', 'confidence': 0.015516051122505486},
        {'name': 'mention_entity', 'confidence': 0.013102384759044393}]},
    {'action': 'action_kbqa'}, 
    {'slots': 
        {'car_series': '旅行家G20', 'attribute': ['市场指导价'], 'car_model': None, 'object_type': None, 'listed_items': None,
        'mention': None, 'mood': None, 'last_actions_name': None, 'last_intent_name': None, 'car_skill': None,
        'last_turn_car_skill': None, 'replay_type': None}}, 
    {'recipient_id': 'default', 'text': '小通为您查询到如下结果:'},
    {'recipient_id': 'default', 'text': "2021款 时光版: {'市场指导价': '309800'}"},
    {'recipient_id': 'default', 'text': "2021款 阳光版: {'市场指导价': '269800'}"}
]





'''