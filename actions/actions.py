# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import os
import json
import jieba
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from knowledge_base.kg_operate import KnowledgeGraphOp
from knowledge_base.schemas import pron_mention, enterprise_info
from knowledge_base.utils import contain_attribute
from FAQ.faq_match import FAQ_match
from FAQ.faq_match import FAQ_BASE_DIR

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
        print('**'*20)

        # 当前子意图
        retrieval_intent = tracker.latest_message['response_selector']['KBQA']['response']['intent_response_key']
        # KBQA/enterprise_information
        if retrieval_intent == 'KBQA/enterprise_information':
            object_type = tracker.get_slot('object_type')
            attribute = tracker.get_slot('attribute')

            flag = contain_attribute(attribute, limit_att=enterprise_info)

            if flag  and object_type is None:
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

                    slots = [SlotSet('object_type', None), SlotSet('listed_items', listed_items), SlotSet('attribute', None)]
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
            last_object_mention = tracker.get_slot('last_object_mention')
            last_attribute_mention = tracker.get_slot('last_attribute_mention')

            # 如果提问的是新车系的话, 则之前的一些插槽需要解决一下
            new_request = car_series != last_object_mention
            if new_request:
                # 在最后返回时，为了下一轮使用car_model信息，所以没有清除，在这里判断一下，如果是新车系，旧的就删除了
                car_model = None




            if mention:
                if listed_items and mention not in pron_mention:
                    # 在指代时,优先找和当前轮最近的主体
                    if listed_items[0] == '车系':
                        car_series = listed_items[int(mention)]


            if not car_series:
                dispatcher.utter_message(template='utter_KBQA/vehicle_information', answer='不好意思，小通需要知道是哪个车系~')
                return []

            # 当上下两句提到的车系不相同时，如果当前没有提问的属性, 则用上一轮的 --》 g20的呢？
            # if car_series != last_object_mention and attribute is None:
            #     attribute = last_attribute_mention

            # to solve example: 第二个的呢
            # if car_series == last_object_mention and attribute is None:
            #     if mention:
            #         attribute = last_attribute_mention

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
                    if mention:
                        if listed_items and mention not in pron_mention:
                            if listed_items[0] == '车型':
                                car_model = listed_items[int(mention)]

                    if car_model is None:
                        # 如果没有具体车型，那么在listed_items中更新指代的车型
                        for k, v in result.items():
                            answer = str(k) + ': ' + str(v)
                            dispatcher.utter_message(template='utter_KBQA/vehicle_information', answer=answer)

                    else:
                        answer = car_model + ': ' + str(result[car_model])
                        dispatcher.utter_message(template='utter_KBQA/vehicle_information', answer=answer)
                else:
                    dispatcher.utter_message(template='utter_KBQA/enterprise_information', answer='抱歉，小通还没学会这个问题，您可以换个问题！')



                slots = [SlotSet('attribute', attribute), SlotSet('car_model', car_model), SlotSet('car_series', car_series),
                         SlotSet('object_type', None), SlotSet('mention', None), SlotSet('last_object_mention', car_series),
                         SlotSet('last_attribute_mention', attribute), SlotSet('listed_items', listed_items)]
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

# class ActionResolveMention(Action):
#     """
#     解决指代问题
#     """
#     def name(self) -> Text:
#         return "action_resolve_mention"
#
#     async def run(self, dispatcher, tracker: Tracker, domain: "DomainDict",) -> List[Dict[Text, Any]]:
#         mention = tracker.get_slot('mention')
#         listed_items = tracker.get_slot('listed_items')
#         last_object_mention = tracker.get_slot('last_object_mention')



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
        print('FAQ match result: {}'.format(result))
        if result == ['', '']:
            dispatcher.utter_message(template='utter_ask_rephrase')

        else:

            answer = result[1]
            dispatcher.utter_message(text=answer)
            # if result['image'] == 'None':
            #     dispatcher.utter_message(text=result['text'])
            # else:
            #     # to do: image的地址合成
            #     img_files = result['image'].split(',')
            #     imgs = []
            #     for img_file in img_files:
            #         imgs.append(os.path.join(FAQ_BASE_DIR, 'data/faq_data/faq_imgs', str(img_file)+'.jpg'))
            #
            #     dispatcher.utter_message(text=result['text'], image=str(imgs))
        return []
