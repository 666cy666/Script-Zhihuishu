import sys
sys.path.append('./Util')
import os
import json
def get_json_info(json_path):
    '''
    获取json文件信息
    :param json_path:
    :return:
    '''
    json_content = {}
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            json_content = json.load(f)
        print(f"从{json_path}读取成功")
    else:
        print(f"json文件不存在{json_path}")
    return json_content

def loading_setting(dict_name, item_name='enabled'):
    '''
    加载json文件
    :param json_path:
    :param dict_name:
    :return:
    '''
    from Util.Settings import config_info_path
    json_info = get_json_info(config_info_path)
    return json_info[dict_name][item_name]

def update_json(json_path,json_info):
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_info, f, ensure_ascii=False, indent=4)
    print(f"json成功写入{json_path}")

def update_json_by_index(json_path, json_info, index):
    if len(json_info) == 0:
        print("json信息为空，请检查变量")
        return
    with open(json_path, 'r', encoding='utf-8') as f:
        json_content = json.load(f)
    json_content[index] = json_info
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_content, f, ensure_ascii=False, indent=4)
    print(f"json成功更新于{json_path}")
