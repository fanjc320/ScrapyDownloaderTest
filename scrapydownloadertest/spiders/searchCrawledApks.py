# -*- coding: utf-8 -*-

# from scrapy.spiders import Spider,CrawlSpider,Rule
# from scrapy.loader import ItemLoader
# from scrapy.selector import Selector
# from scrapy.http import Request
# from scrapy import FormRequest
# from scrapydownloadertest.items import FileDownloadItem, ImgDownloadItem
# from scrapy.utils.response import open_in_browser
# from scrapy.linkextractors import LinkExtractor
# from bs4 import BeautifulSoup
# import sys
# import re
# import os
# import pickle
# import datetime
# from datetime import date, datetime
# from urllib import parse
#
# from selenium import webdriver
# import time
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from zipfile import ZipFile
# import difflib
from crawl_common import *
def searchCrawledApks(dir):
    depth = 1
    for root, dirs, files in os.walk(dir, topdown=True):
        tmp_dir = root[len(dir):]
        # print("tmp_dir:", tmp_dir, " sep count:", tmp_dir.count(os.sep), " root:", root)
        sep_count = root[len(dir):].count(os.sep)
        if sep_count > depth:
            del dirs[:]
            continue
        # print("tmp_dir:", tmp_dir, " sep count:", tmp_dir.count(os.sep), " root-------------------:", root)
        for name in files:
            rootName = os.path.join(root, name)
            # print("searchCrawledApks root:", root, " name:", name)
            packageName, file_ext = os.path.splitext(name)
            suffix = file_ext[1:]
            # print(f"searchCrawledApks rootName:{rootName} 包名: {packageName}, 扩展名:{suffix}, sep_count:{sep_count}")

            if "apk" == suffix:
                print(f"searchCrawledApks apk rootName:{rootName} 包名: {packageName}, 扩展名:{suffix}")
                # continue
                unzipApkAndSearch(root, name)

            if "xapk" == suffix:
                output_folder = unzipApk(root, name)
                # print("searchCrawledApks xapk rootName:", rootName, " packageName:", packageName, " output_folder:",
                #       output_folder)
                for root2, dirs2, files2 in os.walk(output_folder, topdown=True):
                    tmp_dir = root2[len(output_folder):]
                    # print("searchCrawledApks xapk tmp_dir:", tmp_dir, " sep count:", tmp_dir.count(os.sep))
                    if root2[len(output_folder):].count(os.sep) > depth:
                        continue

                    for name3 in files2:
                        rootName3 = os.path.join(root2, name3)
                        packageName3, file_ext = os.path.splitext(name3)
                        # 打印文件名和扩展名
                        suffix3 = file_ext[1:]
                        # print(f"searchCrawledApks xapk rootName:{rootName3} 包名: {packageName3}, 扩展名:{suffix3}")

                        if "apk" == suffix3:
                            unzipApkAndSearch(root2, name3)



searchCrawledApks(apks_dir)


