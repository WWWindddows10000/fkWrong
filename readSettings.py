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
import yaml
import os
from logMeth import log, l


BASE_PATH = r"E:\fkWrong作业文件"

def load_config(path="settings/storeConfigure.fksc"):
    """
    加载YAML
    :return: 存储YAML
    """
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def resolveCode(code,returnPath=True):
    """
    解析文件FID,返回路径
    我看不懂。能跑。
    :param log: socketClient对象
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
                    filename_template = subtype.get("filename", "作业_{编号}.jpg") # 作业（编号）是默认项
                    for arg in subtype["args"]:
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
                        if subtype_name != "未知子类":
                            log("在存储文件（FID为{}）中使用了学期代码：{}，这指代{}。".format(code, term_code, args["学期"]),l.I)
                        else:
                            log("文件（FID为{}）的学期代号（{}）有错误或不存在，归类到未知学期文件夹。".format(code, term_code), l.W)

                    # 拼接路径
                    path_parts = [BASE_PATH]
                    path_parts.append(category["name"])
                    path_parts.append(subtype["name"])
                    if "subtypes" in subtype:
                        sub_code = rest[len(subtype_key):len(subtype_key)+2]
                        subtype_name = subtype["subtypes"].get(sub_code, f"未知子类({sub_code})")
                        if subtype_name != "未知子类":
                            log("在存储文件（FID为{}）中使用了子类代码：{}，这指代{}。".format(code, sub_code, subtype_name),l.I)
                        else:
                            log("文件（FID为{}）的子类代号（{}）有错误或不存在，归类到未知子类文件夹。".format(code, sub_code), l.W)
                        path_parts.append(subtype_name)
                    if "学期" in args:
                        path_parts.append(args["学期"])
                    filename = filename_template.format(**args)
                    path_parts.append(filename)
                    if not returnPath:
                        log("为文件\n{}\n查询了名称：\n{}\n。如果名称不符合实际，以下操作：\n[检查FID或storeConfigure.fksc]\n被建议立即执行。".format(code, os.path.join(*path_parts).replace('\\','-').replace('E:-fkWrong作业文件-','')[:-4]),l.I)
                        return os.path.join(*path_parts).replace('/','-').replace('E:-fkWrong作业文件-','')[:-4]
                    log("已经将文件\nFID为{}\n储存到：\n{}\n。如果路径不符合实际，以下操作：\n[检查FID或storeConfigure.fksc]\n被建议立即执行。".format(code, os.path.join(*path_parts)),l.I)
                    return os.path.join(*path_parts)
    log("无法解析FID：{}。以下操作：\n[检查storeConfigure.fksc]\n被建议立即执行。".format(code), l.E)
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
    log(
        "添加了配置项{}。其属性为：\n父项:{}\n文件名格式:{}\n参数:{}\n子类:{}\n".format(
            code,
            parent if parent is not None else "[无]",
            filename if filename is not None else "[无]",
            args if args is not None else "[无]",
            subtypes if subtypes is not None else "[无]"
        ),
        l.I
    )
    with open("settings/storeConfigure.fksc", 'w', encoding='utf-8') as f:
        yaml.safe_dump(config, f, allow_unicode=True, sort_keys=False)

log("fkWrong! readSettings模块被成功导入。",l.I)
log("现在测试resolveCode函数。",l.I)
try:
    resolveCode('bbghy01202405020152031',False)
except Exception as e:
    log("由于未经处理的异常，无法成功调用resolveCode方法解析FID样例。\n异常信息：{}".format(str(e)),l.F)
    exit(1)