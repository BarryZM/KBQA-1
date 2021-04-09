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



if __name__ == '__main__':
    result = find_head(['上市时间', '车身电子稳定系统',  "能源类型"])
    print(result)