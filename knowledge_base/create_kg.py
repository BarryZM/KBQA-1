from py2neo import Graph, Node, Relationship, NodeMatcher
from py2neo.matching import RelationshipMatcher
import sys
import pandas as pd
from knowledge_base.schemas import schemas

class KnowledgeGraph():
    def __init__(self, url="http://localhost:11004", username='neo4j', password='123456'):
        self.url = url
        self.username = username
        self.password = password
        try:
            self.graph = Graph(self.url, username=self.username, password=self.password)
            print('database connect successful!')
        except:
            raise ValueError('database connnect fail!')

    def create_kg(self, delete_all=False):
        if delete_all:
            print("删除了所有节点和关系!")
            self.graph.run('match (n) detach delete n')
            return True

        print('开始构建知识图谱ing')
        data = pd.read_excel('./brand_data.xlsx', sheet_name=None)

        # 创建品牌节点
        attributes = {}
        sheet = list(data.keys())[-1]
        for index in data[sheet].index:
            attributes[data[sheet].iloc[index]['Question']] = data[sheet].iloc[index]['Answer']

        brand_node = Node('品牌', name='上汽大通', **attributes)
        self.graph.create(brand_node)

        sheets = list(data.keys())[:-1]
        for sheet in sheets:
            print('当前的sheet: {}'.format(sheet))
            data[sheet].set_index('id', inplace=True)

            for index in data[sheet].index:
                # 创建车系节点
                data_sheet = data[sheet].loc[index, '车系']
                car_series_node = self.graph.nodes.match('车系', name=data_sheet).first()
                if car_series_node is None:
                    car_series_node = Node('车系', name=data_sheet)
                    self.graph.create(car_series_node)

                # 车系和品牌的关系
                r = Relationship(brand_node, '车系', car_series_node)
                self.graph.create(r)

                # 创建车型节点
                data_sheet = data[sheet].loc[index, '车型']
                # car_model_node = self.graph.nodes.match('车型', name=data_sheet).first()
                # if car_model_node is None:
                car_model_node = Node('车型', name=data_sheet)
                self.graph.create(car_model_node)

                # 车系和车型边
                r = Relationship(car_series_node, '车型', car_model_node)
                self.graph.create(r)

                # 基本参数节点
                data_field = schemas[sheet]['基本参数'][2:]
                data_sheet = data[sheet].loc[index, data_field]
                attributes = {}
                for schema in data_field:
                    attributes[schema] = str(data_sheet[schema])

                base_parameter_node = self.graph.nodes.match('基本参数', name='基本参数', **attributes).first()
                if base_parameter_node is None:
                    base_parameter_node = Node('基本参数', name='基本参数', **attributes)
                    self.graph.create(base_parameter_node)

                # 基本参数和车型边
                r = Relationship(car_model_node, '基本参数', base_parameter_node)
                self.graph.create(r)

                # 安全配置节点
                data_sheet = data[sheet].loc[index, schemas[sheet]['安全性配置']]

                attributes = {}
                for schema in schemas[sheet]['安全性配置']:
                    attributes[schema] = str(data_sheet[schema])

                safety_node = self.graph.nodes.match('安全性配置', name='安全性配置', **attributes).first()
                if safety_node is None:
                    safety_node = Node('安全性配置', name='安全性配置', **attributes)
                    self.graph.create(safety_node)

                # 安全性配置 和 车型边
                r = Relationship(car_model_node, '安全性配置', safety_node)
                self.graph.create(r)

                #外观与内饰节点
                data_sheet =  data[sheet].loc[index, schemas[sheet]['外观与内饰']]
                attributes = {}
                for schema in schemas[sheet]['外观与内饰']:
                    attributes[schema] = str(data_sheet[schema])

                appearance_node = self.graph.nodes.match('外观与内饰', name='外观与内饰', **attributes).first()
                if appearance_node is None:
                    appearance_node = Node('外观与内饰', name='外观与内饰', **attributes)
                    self.graph.create(appearance_node)
                # 外观节点和 车型 边
                r = Relationship(car_model_node, '外观与内饰', appearance_node)
                self.graph.create(r)

                # 舒适与便利节点
                data_sheet = data[sheet].loc[index, schemas[sheet]['舒适与便利']]
                attributes = {}
                for schema in schemas[sheet]['舒适与便利']:
                    attributes[schema] = str(data_sheet[schema])

                comfortable_node = self.graph.nodes.match('舒适与便利', name='舒适与便利', **attributes).first()
                if comfortable_node is None:
                    comfortable_node = Node('舒适与便利', name='舒适与便利', **attributes)
                    self.graph.create(comfortable_node)
                # 舒适 和 车型边
                r = Relationship(car_model_node, '舒适与便利', comfortable_node)
                self.graph.create(r)

        print('构建完成！')







if __name__ == '__main__':
    kg = KnowledgeGraph()
    kg.create_kg(delete_all=False)