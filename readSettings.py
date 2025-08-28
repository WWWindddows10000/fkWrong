# Settings recognition 
"""
███████╗██╗  ██╗██╗    ██╗██████╗  ██████╗ ███╗   ██╗ ██████╗ 
██╔════╝██║ ██╔╝██║    ██║██╔══██╗██╔═══██╗████╗  ██║██╔════╝ 
█████╗  █████╔╝ ██║ █╗ ██║██████╔╝██║   ██║██╔██╗ ██║██║  ███╗
██╔══╝  ██╔═██╗ ██║███╗██║██╔══██╗██║   ██║██║╚██╗██║██║   ██║
██║     ██║  ██╗╚███╔███╔╝██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝
╚═╝     ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝                                                       
fkWrong! SettingsReco version 0.1.0                                        
"""
import os
import json
from logMeth import log, l

BASE_PATH = r"E:\fkWrong作业文件"

def load_config(path="settings/storeConfigure.fksc"):
    """
    加载JSON
    :return: 存储JSON
    """
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config, path="settings/storeConfigure.json"):
    """
    保存JSON
    """
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def resolveCode(code, returnPath=True):
    """
    解析文件FID,返回路径
    :param code: FID
    :param returnPath: 是否返回路径，否则返回文件名
    :return: 路径
    """
    config = load_config()
    for prefix in config:
        if prefix == '学期':
            continue
        if code.startswith(prefix):
            category = config[prefix]
            rest = code[len(prefix):]

            for subtype_key, subtype_data in category.items():
                if not isinstance(subtype_data, dict):  # 跳过 name 字段
                    continue
                if rest.startswith(subtype_key):
                    subtype = subtype_data
                    args = {}
                    filename_template = subtype.get("filename", "作业_{编号}.jpg")

                    for arg in subtype.get("args", []):
                        name = arg["name"]
                        index = arg["index"]
                        length = arg["length"]
                        if index == -1:
                            args[name] = code[-length:]
                        elif length == -1:
                            args[name] = code[index:-1]
                        elif length == 99:
                            args[name] = code[index:]
                        else:
                            args[name] = code[index:index+length]

                    # 映射学期名
                    if "学期" in args:
                        term_code = str(args["学期"])
                        args["学期"] = config["学期"].get(term_code, f"未知学期({term_code})")

                    # 拼接路径
                    path_parts = [BASE_PATH]
                    path_parts.append(category["name"])
                    path_parts.append(subtype["name"])
                    subtype_name = None
                    if "subtypes" in subtype:
                        sub_code = rest[len(subtype_key):len(subtype_key)+2]
                        subtype_name = subtype["subtypes"].get(sub_code, f"未知子类({sub_code})")
                        path_parts.append(subtype_name)
                    if "学期" in args:
                        path_parts.append(args["学期"])
                    filename = filename_template.format(**args)
                    path_parts.append(filename)

                    if not returnPath:
                        return os.path.join(*path_parts).replace('\\', '-').replace('E:-fkWrong作业文件-', '')[:-4]
                    return os.path.join(*path_parts)
    return 0

def addToConf(parent, code, name, filename=None, args=None, subtypes=None):
    """
    添加新的配置项到配置文件中
    """
    config = load_config()

    entry = {"name": name}
    if filename is not None:
        entry["filename"] = filename
    if args is not None:
        entry["args"] = args
    if subtypes is not None:
        entry["subtypes"] = subtypes

    if not parent:
        config[code] = entry
    else:
        if parent not in config:
            config[parent] = {"name": parent}
        config[parent][code] = entry

    save_config(config)

def resolveAsTree():
    config = load_config()
    tree = []

    for main_id, main_val in config.items():
        if main_id == "学期":
            continue

        main_name = main_val.get("name", main_id)
        main_node = {
            "id": main_id,
            "name": main_name,
            "father": "（根节点）",
            "children": []
        }

        for sub_id, sub_val in main_val.items():
            if sub_id == "name":
                continue
            if not isinstance(sub_val, dict):
                continue

            sub_node = {
                "id": f"{main_id}_{sub_id}",
                "name": sub_val.get("name", sub_id),
                "father": main_id,
            }
            if "args" in sub_val:
                sub_node["args"] = sub_val["args"]

            # 子类
            if "subtypes" in sub_val:
                sub_node["children"] = []
                for subtype_code, subtype_name in sub_val["subtypes"].items():
                    sub_node["children"].append({
                        "id": f"{main_id}_{sub_id}_{subtype_code}",
                        "name": subtype_name,
                        "father": f"{main_id}_{sub_id}"
                    })

            main_node["children"].append(sub_node)

        tree.append(main_node)

    return tree
