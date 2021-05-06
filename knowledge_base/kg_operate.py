from py2neo import Graph, Node, Relationship, NodeMatcher
from py2neo.matching import RelationshipMatcher
from knowledge_base.utils import *
import sys

class KnowledgeGraphOp():
    def __init__(self):
        try:
            self.graph = Graph("http://localhost:7474", username='neo4j', password='123456')
            print("database connect successful!")
        except:
            raise ValueError('database connect fail!')

    def query_nodes(self, label, entity_name=None, attribute=None, relationship=None, limit_num=10):
        """
        1.按照label和attribute来查询节点
        2.按照relationship来实现跨边的节点查询
        """
        result = []
        if entity_name:
            if relationship:
                node = self.graph.nodes.match(label, name=entity_name).first()
                nodes = self.graph.match(nodes=(node, None), r_type=relationship).limit(limit_num).all()
                for node in nodes:
                    result.append(node.end_node['name'])

        else:
            if attribute is None and relationship:
                nodes = self.graph.match(r_type=relationship).limit(limit_num).all()
                for node in nodes:
                    result.append(node.end_node['name'])

        return result

    def query_attribute(self, label, entity_name=None, attribute=None, relationship=None, limit_num=10):
        '''

        :param label:
        :param entity_name: 起始节点的名称
        :param attribute:
        :param relationship: 判断是否要跨边查询，例如 is True: 由车系-->车型-->基本参数  is False: 车型-->基本参数
        :param limit_num:
        :return:
        '''

        if relationship:
            node_entity = self.graph.nodes.match(label, name=entity_name).first()
            nodes = self.graph.match(nodes=(node_entity, None), r_type=relationship).limit(limit_num).all()
            result = {}

            for node in nodes:
                result_cache = {}
                att_heads = find_head(attribute)
                for k, v in att_heads.items():
                    node_tail = self.graph.match(nodes=(node.end_node, None), r_type=k).limit(limit_num).first()
                    for i, att in enumerate(attribute):
                        if i in v:
                            result_cache[att] = node_tail.end_node[att]

                # for att in attribute:
                #     result_cache[att] = node.end_node[att]
                result[node.end_node['name']] = result_cache

        else:
            node_entity = self.graph.nodes.match(label, name=entity_name).first()
            result = {}
            if label == '品牌':
                for i, att in enumerate(attribute):
                    result[att] = node_entity.end_node[att]

            att_heads = find_head(attribute)

            for k, v in att_heads.items():
                node = self.graph.match(nodes=(node_entity, None), r_type=k).limit(limit_num).first()
                for i, att in enumerate(attribute):
                    if i in v:
                        result[att] = node.end_node[att]

            # result = {}
            # for att in attribute:
            #     result[att] = node.end_node[att]


        return result


if __name__ == '__main__':
    kg = KnowledgeGraphOp()
    result = kg.query_nodes(label='品牌', relationship='车系')
    # result = kg.query_nodes(label='车系', entity_name='旅行家G20', relationship='车型')
    print("query_node 结果: {}".format(result))

    result = kg.query_attribute("车型", entity_name='2021款 舒享版', attribute=['上市时间', '发动机型式', "车身电子稳定系统"])
    # result = kg.query_attribute(label="车系", entity_name='旅行家G20', attribute=['上市时间', '市场指导价', "车身电子稳定系统"], relationship='车型')
    # result = kg.query_attribute('品牌', entity_name='上汽大通', attribute=['售后电话'])
    print("query_attribute 结果: {}".format(result))