# -*- coding: utf-8 -*-

from scrapy.spiders import Spider,CrawlSpider,Rule
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import FormRequest
from scrapydownloadertest.items import FileDownloadItem, ImgDownloadItem
from scrapy.utils.response import open_in_browser
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import sys
import re
import os
import pickle
import datetime
from datetime import date, datetime
from urllib import parse

from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from zipfile import ZipFile
import difflib

# 参考https://stackoverflow.com/questions/70583894/cannot-click-a-button-using-python-selenium-on-a-certain-website
apks_dir = r"E:\crawl_apks"
def searchAssembly(lib_path):
    foundAssembly = 0
    # print("lib_path:", lib_path)
    for r, d, f in os.walk(lib_path, topdown= True):
        fileCnt = len(f)
        print("lib so fileCount:", fileCnt, " so:", f)
        if fileCnt == 0:
            print("searchAssembly lib_path error!!!!!")
        for so in f:
            if "libil2cpp" in so:
                print("found libil2cpp.so")
                foundAssembly = 1
                break
            elif "libmono" in so:
                print("found libmono*.so")
                foundAssembly = 2
                break
            elif "libunity" in so:
                print("found libunity.so")
                foundAssembly = 3
                break
            elif "libcocos" in so:
                print("found libcocos*.so")
                foundAssembly = 3
                break
            # else:
            #     print("found no unity")
            if "lua" in so:
                print("found lua")
                foundAssembly *= 10
                break
    return foundAssembly

def unzipApk(root, name): # dir, apkName
    rootName = os.path.join(root, name)
    with ZipFile(rootName, 'r') as f:
        # print("unzipApk extract name:", rootName)
        packageName, file_ext = os.path.splitext(name)
        output_folder = os.path.join(root, packageName)
        os.makedirs(output_folder, exist_ok=True)
        f.extractall(output_folder + "")
        # print("unzipApk output_folder:", output_folder)
    return output_folder
def unzipApkAndSearch(root, name): # dir,apkname
    output_folder = unzipApk(root, name)
    rootName = os.path.join(root, name)
    # print("unzipApkAndSearch rootName:", rootName, " output_folder:", output_folder)

    lib_path1 = os.path.join(output_folder, "lib\\armeabi-v7a")
    lib_path2 = os.path.join(output_folder, "lib\\arm64-v8a")
    lib_path3 = os.path.join(output_folder, "lib\\x86")
    if os.path.exists(lib_path1):
        lib_path = lib_path1
    elif os.path.exists(lib_path2):
        lib_path = lib_path2
    elif os.path.exists(lib_path3):
        lib_path = lib_path3
    else:
        # print("no lib, no unity")
        return

    res = searchAssembly(lib_path)
    # print("unzipApkAndSearch rootName:", rootName, " result:", res)

def getAllCrawledApks(dir):
    dic_all_crawled_apks = []
    depth = 1
    for root, dirs, files in os.walk(dir, topdown=True):
        tmp_dir = root[len(dir):]
        sep_count = tmp_dir.count(os.sep)
        print("getAllCrawledApks tmp_dir:", tmp_dir, " sep count:", sep_count, " files:", files)
        if sep_count > depth:
            del dirs[:]
            continue
        for apk in files:
            apkName, file_ext = os.path.splitext(apk)
            suffix = file_ext[1:]
            print("getAllCrawledApks apk:",apk, " apkName:", apkName, " suffix:", suffix, " tmp_dir:", tmp_dir)
            if suffix == "apk" or suffix == "xapk":
                dic_all_crawled_apks.append(apk)
    print("getAllCrawledApks dic_all_crawled_apks:", dic_all_crawled_apks)
    return dic_all_crawled_apks

def closeAd(browser):
    frames = browser.find_elements(By.TAG_NAME, "iframe")
    for frame in frames:
        try:
            frameLabel = frame.get_attribute("aria-label") #
            frameId = frame.get_attribute("id") #
            frameStyle = frame.get_attribute("style")
            print("frameLabel:", frameLabel, " id:", frameId)
            if frameLabel == "Advertisement" and "max-height" in frameStyle:
                print("switch to frame swift")
                browser.switch_to.frame(frame)

                try:
                    dismissBtn = browser.find_element(By.XPATH, '//*[@id="dismiss-button"]')
                    if dismissBtn:
                        # print("dismissBtn:", dismissBtn)
                        dismissBtn.click()
                    break  # Exit loop once you switch to the correct frame
                except:
                    framesAd = browser.find_elements(By.TAG_NAME, "iframe")
                    for frameAd in framesAd:
                        frameAdId = frameAd.get_attribute("id")
                        print("frameAdId:", frameAdId)
                        if frameAdId == "ad_iframe":
                            print("switch to frame Ad")
                            browser.switch_to.frame(frameAd)

                            dismissBtn = browser.find_element(By.XPATH, '//*[@id="dismiss-button"]')
                            if dismissBtn:
                                print("dismissBtn:", dismissBtn)
                                dismissBtn.click()
                            break  # Exit loop once you switch to the correct frame
        except:
            print("closeAd iframe except!")

    browser.switch_to.default_content()

# def searchApkInternal(dir):
#     found = False
#     for root, dirs, files in os.walk(dir, topdown=False):
#         dir_dic = []
#         for dir in dirs:
#             dir_dic[str(dir)] = dir
#         for name in files:
#             print(os.path.join(root, name))
#             # 判断是否为文件（排除文件夹）
#             # if os.path.isfile(name):
#             # 使用os.path.splitext()获取文件名和扩展名
#             file_base_name, file_ext = os.path.splitext(name)
#             # 打印文件名和扩展名
#             suffix = file_ext[1:]
#             print(f"文件名: {file_base_name}, 扩展名: {suffix}")
#             # if apkName in file_base_name and "apk" == suffix:
#             apkName = file_base_name
#             if "apk" == suffix:
#                 found = True
#                 print("apk:", apkName, " download complete")
#                 if apkName in dir_dic:
#                     print("apkName in dir_dic, apkName:", apkName)
#                 else:
#                     with ZipFile(apkName, 'r') as f:
#                         print("extract apk:", apkName)
#                         f.extractall()
#


# #####searchApkInternal(apks_dir)
# getAllCrawledApks(apks_dir)

#0.771
# str1 = "Crazy Driver 3D_ Car Traffic_2.7.1_APKPure"
# str2 = "Crazy Driver 3D: Car Traffic"

#1.0
# str1 = "Crazy Driver 3D_ Car Traffic"
# str2 = "Crazy Driver 3D_ Car Traffic"

#0.96
# str1 = "Crazy Driver 3D_ Car Traffi"
# str2 = "Crazy Driver 3D Car Traffic"

# difflib 去掉列表中不需要比较的字符
# seq = difflib.SequenceMatcher(lambda x: x in ' _:', str1, str2)
# ratio = seq.ratio()
# print('difflib similarity2: ', ratio)

# str1 = "Merge Forest - Merge Games_1.5.0_APKPure.apk"
# str2 = "Crazy Driver 3D: Car Traffic"
#
# apkSub = str1[0:len(str2)]
# apkName = str2
# seq = difflib.SequenceMatcher(lambda x: x in " -_:", apkSub, apkName)
# ratio = seq.ratio()
# print('difflib apksub:', apkSub, 'apkName', apkName, ' similarity: ', ratio)



