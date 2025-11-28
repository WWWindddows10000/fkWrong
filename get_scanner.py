import pythoncom
import win32com.client
from logging_methods import l, log

def get_scanners():
    """获取所有扫描仪设备列表"""
    try:
        log("Fetching scanners", l.I)
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
        log(f"Found {len(scanners)} scanners", l.D)
        return scanners

    except Exception as e:
        log(f"获取扫描仪列表失败: {e}", l.W)
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
                log(f"已选择扫描仪: {scanner['name']}", l.I)
                return device
            except Exception as e:
                log(f"连接扫描仪失败: {e}", l.E)
                return None
            finally:
                pythoncom.CoUninitialize()
    log(f"未找到名称为 '{scanner_name}' 的扫描仪", l.E)
    return None


class Scanner:
    def __init__(self):
        self.scan_name = "untitled_scan.png"
        self.scanner = "default"
        self.dpi = 400
        select_scanner_by_name(self.scanner)
