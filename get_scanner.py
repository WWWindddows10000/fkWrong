import pythoncom
import win32com.client
from logging_methods import l, log

def get_scanners():
    """获取所有扫描仪设备列表"""
    try:
        pythoncom.CoInitialize()
        device_manager = win32com.client.Dispatch("WIA.DeviceManager")
        scanners = []
        for device_info in device_manager.DeviceInfos:
            try:
                if device_info.Type == 1:   # 不确定是否应为1
                    scanners.append({
                        "name": device_info.Properties("Name").Value,
                        "id": device_info.DeviceID,
                        "description": device_info.Properties("Description").Value
                    })
            except Exception as e:
                log(f"[get_scanner.py] Failed to reach scanner information: {e}",l.E)
                raise

        return scanners

    except Exception as e:
        print(f"获取扫描仪列表失败: {e}")
        return []

    finally:
        # 释放COM环境
        pythoncom.CoUninitialize()


class Scanner:
    def __init__(self):
        self.scan_name = "untitled_scan.png"
        self.scanner = "default"
        self.dpi = 400

"""
import pythoncom
import win32com.client

def get_scanners():
    try:
        # 初始化COM环境
        pythoncom.CoInitialize()
        
        # 创建WIA设备管理器
        device_manager = win32com.client.Dispatch("WIA.DeviceManager")
        
        scanners = []
        # 遍历所有设备
        for device_info in device_manager.DeviceInfos:
            try:
                # 设备类型：1 = 扫描仪，2 = 相机（不同版本可能有差异，建议实测）
                if device_info.Type == 1:
                    scanners.append({
                        "name": device_info.Properties("Name").Value,
                        "id": device_info.DeviceID,
                        "description": device_info.Properties("Description").Value
                    })
            except Exception as e:
                print(f"获取设备信息失败: {e}")
                continue
        
        return scanners
    
    except Exception as e:
        print(f"获取扫描仪列表失败: {e}")
        return []
    
    finally:
        # 释放COM环境
        pythoncom.CoUninitialize()

def select_scanner_by_name(scanner_name):
    scanners = get_scanners()
    for scanner in scanners:
        if scanner_name in scanner["name"]:  # 模糊匹配（可改为精确匹配 ==）
            try:
                # 初始化COM环境
                pythoncom.CoInitialize()
                # 连接到指定扫描仪
                device_manager = win32com.client.Dispatch("WIA.DeviceManager")
                device = device_manager.DeviceInfos(scanner["id"]).Connect()
                print(f"已选择扫描仪: {scanner['name']}")
                return device
            except Exception as e:
                print(f"连接扫描仪失败: {e}")
                return None
            finally:
                pythoncom.CoUninitialize()
    print(f"未找到名称为 '{scanner_name}' 的扫描仪")
    return None

# 使用示例
if __name__ == "__main__":
    # 获取所有扫描仪
    all_scanners = get_scanners()
    print("所有扫描仪列表:")
    for idx, scanner in enumerate(all_scanners, 1):
        print(f"{idx}. 名称: {scanner['name']}, ID: {scanner['id']}")
    
    # 选择指定名称的扫描仪（替换为你的扫描仪名称）
    target_scanner = "HP LaserJet MFP M126nw"  # 示例名称
    selected_device = select_scanner_by_name(target_scanner)
    
    if selected_device:
        # 这里可以添加扫描操作代码（如获取扫描项等）
        print("扫描仪连接成功，可执行扫描操作")
"""