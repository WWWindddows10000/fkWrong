# HW scanning
"""
███████╗██╗  ██╗██╗    ██╗██████╗  ██████╗ ███╗   ██╗ ██████╗ 
██╔════╝██║ ██╔╝██║    ██║██╔══██╗██╔═══██╗████╗  ██║██╔════╝ 
█████╗  █████╔╝ ██║ █╗ ██║██████╔╝██║   ██║██╔██╗ ██║██║  ███╗
██╔══╝  ██╔═██╗ ██║███╗██║██╔══██╗██║   ██║██║╚██╗██║██║   ██║
██║     ██║  ██╗╚███╔███╔╝██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝
╚═╝     ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝                                                       
fkWrong! HWscan version 0.1.0                                        
"""
import fitz 
import os
import shutil
from pyzbar.pyzbar import decode
from PIL import Image
from logMeth import log, l
from readSettings import resolveCode

def loadPDF(pdfPath):
    """
    从指定路径获取pdf文件,置入temp
    :param pdfPath: PDF路径
    :return: 总页数
    """
    pdfDocument = fitz.open(pdfPath)
    for page in range(len(pdfDocument)):
        page = pdfDocument.load_page(page)
        imageList = page.get_images(full=True)
        if not imageList:
            log(f"Page {page + 1} has no images.", l.W)
            continue
        for imgIndex, img in enumerate(imageList):
            xref = img[0]
            baseImage = pdfDocument.extract_image(xref)
            imageBytes = baseImage["image"]
            imageExt = baseImage["ext"]
            imageFilename = f"temp/imageLin_{page + 1}.{imageExt}"
            with open(imageFilename, "wb") as imageFile:
                imageFile.write(imageBytes)
    return len(pdfDocument)
    
def scan_barcodes_in_temp(pdfPath):
    loadPDF(pdfPath)
    temp_folder = "temp"
    result = {}
    for filename in os.listdir(temp_folder):
        file_path = os.path.join(temp_folder, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img = Image.open(file_path)
            barcodes = decode(img)
            for barcode in barcodes:
                info = barcode.data.decode("utf-8")
                result[info] = file_path 
    for filename in os.listdir(temp_folder):
        file_path = os.path.join(temp_folder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    return result

def copy_image(src_path, dst_dir):
    """
    复制图片到目标目录，如果目录不存在则自动创建
    :param src_path: 源图片路径
    :param dst_dir: 目标文件夹路径
    :return: 目标图片路径
    """
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    dst_path = os.path.join(dst_dir, os.path.basename(src_path))
    shutil.copy(src_path, dst_path)
    return dst_path

def sort(FID, pic):
    path = resolveCode(FID)
    