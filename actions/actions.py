# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import os
import json

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from knowledge_base.kg_operate import KnowledgeGraphOp
from FAQ.faq_match import FAQ_match

class ActionKBQA(Action):
    def __init__(self):
        self.KGOp = KnowledgeGraphOp()

    def name(self) -> Text:
        return "action_kbqa"

    async def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        print("状态跟踪信息:")
        print(tracker.latest_message)

        print("插槽填充情况:")
        print(tracker.slots)

        print("当前*主*意图：")
        print(tracker.latest_message['intent']['name'])

        print("当前*子*意图：")
        print(tracker.latest_message['response_selector']['KBQA']['response']['intent_response_key'])

        print("当前*子*意图回复模板：")
        retrieval_intent_templete = tracker.latest_message['response_selector']['KBQA']['response']['template_name']
        print(retrieval_intent_templete)

        # 当前子意图
        retrieval_intent = tracker.latest_message['response_selector']['KBQA']['response']['intent_response_key']
        # KBQA/enterprise_information
        if retrieval_intent == 'KBQA/enterprise_information':
            object_type = tracker.get_slot('object_type')
            attribute = tracker.get_slot('attribute')

            if attribute and object_type is None:
                result = self.KGOp.query_attribute('品牌', entity_name='上汽大通', attribute=attribute)
                # 防止result为空
                if len(result) != 0:
                    dispatcher.utter_message(template='utter_KBQA/enterprise_information', answer='小通为您查询到:')
                    for k, v in result.items():
                        answer = k + ': ' + v
                        dispatcher.utter_message(template='utter_KBQA/enterprise_information', answer=answer)
                    slots = [SlotSet('attribute', None)]
                    return slots
                else:
                    dispatcher.utter_message(template='utter_KBQA/enterprise_information', answer='抱歉，小通还没学会这个问题，您可以换个问题！')
                    slots = [SlotSet('attribute', None)]
                    return slots


            # 查询 车系信息
            else:
                result = self.KGOp.query_nodes(label='品牌', relationship='车系')
                # 防止result为空
                if len(result) != 0:
                    dispatcher.utter_message(template='utter_KBQA/enterprise_information', answer='小通为您找到了下列车系:')
                    listed_items = ['车系']
                    for k, v in enumerate(result):
                        answer = str(k + 1) + ": " + v
                        listed_items.append(v)
                        dispatcher.utter_message(template='utter_KBQA/enterprise_information', answer=answer)

                    slots = [SlotSet('object_type', None), SlotSet('listed_items', listed_items)]
                    return slots


                else:
                    dispatcher.utter_message(template='utter_KBQA/enterprise_information', answer='抱歉，小通还没学会这个问题，您可以换个问题！')
                    slots = [SlotSet('object_type', None)]
                    return slots



        elif retrieval_intent == 'KBQA/vehicle_information':
            # 获取需要的插槽值
            car_series = tracker.get_slot('car_series')
            object_type = tracker.get_slot('object_type')
            attribute = tracker.get_slot('attribute')
            car_model = tracker.get_slot('car_model')
            mention = tracker.get_slot('mention')
            listed_items = tracker.get_slot('listed_items')

            if listed_items and mention:
                if listed_items[0] == '车系':
                    car_series = listed_items[int(mention)]

            if not car_series:
                dispatcher.utter_message(template='utter_KBQA/vehicle_information', answer='不好意思，小通需要知道是哪个车系~')
                return []

            # 查询 由车系查车型信息
            if object_type:
                # 查车系节点 -》车型 -》车型节点
                result = self.KGOp.query_nodes(label='车系', entity_name=car_series, relationship=object_type)
                # 防止result为空
                if len(result) != 0:
                    dispatcher.utter_message(template='utter_KBQA/vehicle_information', answer='小通为您查到下列车型:')
                    listed_items = ['车型']
                    for k, v in enumerate(result):
                        answer = str(k+1) + ': ' + v
                        listed_items.append(v)
                        dispatcher.utter_message(template='utter_KBQA/vehicle_information', answer=answer)

                    slots = [SlotSet('listed_items', listed_items), SlotSet('object_type', None)]
                    return slots

                else:
                    dispatcher.utter_message(template='utter_KBQA/enterprise_information', answer='抱歉，小通还没学会这个问题，您可以换个问题！')
                    slots = [SlotSet('object_type', None)]
                    return slots

            # 查询车系或者车型的属性
            elif attribute:

                # G20的市场价格是多少 ==》将G20所有车型的价格返回 ==》G20-->车型-->属性
                result = self.KGOp.query_attribute(label='车系', entity_name=car_series, attribute=attribute, relationship='车型')
                # 防止result为空
                if len(result) != 0:
                    dispatcher.utter_message(template='utter_KBQA/vehicle_information', answer='小通为您查询到如下结果:')
                    # 判断是否是具体的某个车型
                    # 确定指代
                    if listed_items and mention:
                        if listed_items[0] == '车型':
                            car_model = listed_items[int(mention)]

                    if car_model is None:
                        for k, v in result.items():
                            answer = str(k) + ': ' + str(v)
                            dispatcher.utter_message(template='utter_KBQA/vehicle_information', answer=answer)

                    else:
                        answer = car_model + ': ' + str(result[car_model])
                        dispatcher.utter_message(template='utter_KBQA/vehicle_information', answer=answer)
                else:
                    dispatcher.utter_message(template='utter_KBQA/enterprise_information', answer='抱歉，小通还没学会这个问题，您可以换个问题！')


                slots = [SlotSet('attribute', None), SlotSet('car_model', None), SlotSet('car_series', car_series),
                         SlotSet('object_type', None), SlotSet('mention', None)]
                return slots

            else:
                dispatcher.utter_message(template='utter_ask_rephrase')
                return []

        else:
            dispatcher.utter_message(template='utter_ask_rephrase')
            return []


class ActionResolveMention(Action):
    """
    解决顺序指代问题
    """
    def name(self) -> Text:
        return "action_resolve_mention"

    async def run(self, dispatcher, tracker: Tracker, domain: "DomainDict",) -> List[Dict[Text, Any]]:
        listed_items = tracker.get_slot('listed_items')
        mention = tracker.get_slot('mention')
        if mention is not None and listed_items is not None:
            index = int(mention)
            answer = "好的，已为您锁定 " + listed_items[index]
            dispatcher.utter_message(text=answer)
        else:
            dispatcher.utter_message(template='utter_ask_rephrase')

        slots = [SlotSet('mention', None)]
        return slots

class ActionFAQ(Action):
    """
    解决FAQ问题
    """
    def __init__(self):
        self.match = FAQ_match()

    def name(self) -> Text:
        return "action_faq"

    async def run(self, dispatcher, tracker: Tracker, domain: "DomainDict",) -> List[Dict[Text, Any]]:
        # match = FAQ_match()
        message = tracker.latest_message['text']
        result = self.match.faq_match(message)
        print(result)
        if result == []:
            dispatcher.utter_message(template='utter_ask_rephrase')
        else:
            result = json.loads(result[1])
            if result['image'] == 'None':
                dispatcher.utter_message(text=result['text'])
            else:
                # to do: image的地址合成
                dispatcher.utter_message(text=result['text'], image=result['image'])
        return []
