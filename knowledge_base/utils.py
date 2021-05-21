from knowledge_base.schemas import schemas
import json

def find_head(attribute):
    '''
    找到属性所对应节点
    :param attribute: list
    :return: dict{att_head: [index of att_head]}
    '''
    att_heads = []
    for att in attribute:
        for k, v in dict(list(schemas.values())[0]).items():
            if att in v:
                att_heads.append(k)

    result = {}
    result = result.fromkeys(set(att_heads))
    for k in result.keys():
        v = [i for i, x in enumerate(att_heads) if x == k]
        result[k] = v

    return result

def composite_attribute(attribute):
    rules = ['外观', '颜色']
    if rules[0] in attribute and rules[1] in attribute:
        attribute = '外观颜色'

    return attribute

def contain_attribute(attribute, limit_att):
    '''
    判断 attribute 是否 有 att 在 limit_att 中
    :param attribute:
    :param limit_att:
    :return:
    '''
    flag = False
    if attribute:
        for att in attribute:
            if att in limit_att:
                flag = True
                break

    return flag

def check_query_result(result):
    """
    判断 neo4j 查询结果是否为空
    :param result: {'car model':{ 'att1': value}, 'car model':{'att2': value}} or list []
    :return:
    """
    if isinstance(result, dict):
        result_keys = result.keys()
        if len(result_keys) == 0:
            return False

        result_values = result.values()
        for v in result_values:
            if v != {}:
                return True

        return False

    if isinstance(result, list):
        if len(result) == 0:
            return False
        else:
            return True









if __name__ == '__main__':
    result = find_head(['上市时间', '车身电子稳定系统',  "能源类型"])
    result = check_query_result({'car model 1':{1:3}, 'car model 2':{ }})
    print(result)