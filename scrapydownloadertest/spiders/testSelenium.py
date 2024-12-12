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

# 参考https://stackoverflow.com/questions/70583894/cannot-click-a-button-using-python-selenium-on-a-certain-website

def baseTest():
    browser = webdriver.Chrome()
    browser.get(r'https://www.baidu.com/')
    # 设置分辨率 500*500
    browser.set_window_size(500,500)
    time.sleep(2)

    # 打开淘宝页面
    browser.get('https://www.bilibili.com/')
    time.sleep(2)

    # 后退到百度页面
    browser.back()
    time.sleep(2)

    # 前进的淘宝页面
    browser.forward()
    # 网页标题
    print(browser.title)
    # 当前网址
    print(browser.current_url)
    # 浏览器名称
    print(browser.name)
    # 网页源码
    print(browser.page_source)

    time.sleep(2)

    browser.close()

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
        print("no lib, no unity")
        return

    res = searchAssembly(lib_path)
    print("unzipApkAndSearch rootName:", rootName, " result:", res)

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


def closeAd(browser):
    frames = browser.find_elements(By.TAG_NAME, "iframe")
    for frame in frames:
        try:
            frameLabel = frame.get_attribute("aria-label") #
            frameId = frame.get_attribute("id") #
            frameStyle = frame.get_attribute("style")
            # print("frameLabel:", frameLabel, " id:", frameId)
            if frameLabel == "Advertisement" and "max-height" in frameStyle:
                # print("switch to frame swift")
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
                        # print("frameAdId:", frameAdId)
                        if frameAdId == "ad_iframe":
                            # print("switch to frame Ad")
                            browser.switch_to.frame(frameAd)

                            dismissBtn = browser.find_element(By.XPATH, '//*[@id="dismiss-button"]')
                            if dismissBtn:
                                # print("dismissBtn:", dismissBtn)
                                dismissBtn.click()
                            break  # Exit loop once you switch to the correct frame
        except:
            print("closeAd iframe except!")

    browser.switch_to.default_content()


apks_dir = r"E:\crawl_apks"
def TestApkpure():
    option = webdriver.ChromeOptions()

    prefs = {
        "download.default_directory": apks_dir,
        "profile.default_content_setting_values.automatic_downloads": 1,  # 允许多文件下载
        # 无用 "debuggerAddress": "127.0.0.1:62271" #只打开一个浏览器实例 chrome所在路劲\chrome.exe --remote-debugging-port=12306 https://blog.csdn.net/Qwertyuiop2016/article/details/103488817
    }

    option.add_experimental_option("prefs", prefs)
    option.add_experimental_option("detach", True)
    option.add_argument("disable-popup-blocking")
    browser = webdriver.Chrome(options=option)

    # browser.get(r'https://apkpure.com/game_casual')
    browser.get(r'https://apkpure.com/cn/game_casual')
    print("TestApkpure window handle:", browser.current_window_handle)
    # 最近更新的游戏
    xpath_latestGames = '/html/body/main/div[5]/div[2]/div[1]/div/div/ul/li/div/a[1]'
    latestGames = WebDriverWait(browser, 4, 0.2).until(lambda x: x.find_elements(By.XPATH, xpath_latestGames))
    # print("xpath_latestGames:", latestGames)
    # latestGames = browser.find_elements(By.XPATH, xpath_latestGames)
    # latestGames = browser.find_elements_by_xpath(By.XPATH,'//main/div[5]/div[2]/div[1]/div/div/ul/li/div/a[contains(@class, "apk-grid-button")]')
    print("latestGames:", latestGames)

    try:
        element = WebDriverWait(browser, 4, 0.2).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="policy-info"]/div/div[@class="btn"]/span[1]'))
            # EC.element_to_be_clickable((By.XPATH, '//div[@id="policy-info"]/div/div[@class="btn"]/span[1]'))
        )
        if not element:
            print("no find accept all cookies btn")
        element.click()
        print("accept all cookies >>>")
    except:
        print("no accept all cookies <<<<<")

    js_code = 'window.scrollBy(0, 200)'  # 滑动指定距离
    # js_code = 'window.scrollBy(0, document.body.scrollHeight)'  # 滑动到底
    browser.execute_script(script=js_code)

    dic_package = {}
    # today = datetime.date.today()
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    print(date_string)  # Output: 2023-09-15 14:45:30
    dbName = 'dic_package_'+date_string+'.pkl'
    try:
        with open(dbName, 'rb') as f:
            dic_package = pickle.load(f)
            print("dic_package read ok!")
    except IOError:
        print("no file dic_package")
    for i in range(len(latestGames)):
        # if count > 5:
        #     break
        print("count:", i)
        # browser.implicitly_wait(5)
        browser.switch_to.window(browser.window_handles[0])
        item = latestGames[i]

        href = item.get_attribute("href")
        # 判断元素是否可以点击
        # answer = item.is_enabled()
        print("href:", href)
        # print(f'item:{i}:\t{item} latestGames:{latestGames}')

        # item.screenshot("item.png")

        # 以下代码经常无法打开新的标签，而是在首页上打开
        # ActionChains(browser).key_down(Keys.CONTROL).click(item).key_up(Keys.CONTROL).perform()
        # ActionChains(browser).move_to_element(item).key_down(Keys.CONTROL).click(item).key_up(Keys.CONTROL).perform()

        browser.execute_script("window.open('');")
        window_numb = len(browser.window_handles)
        browser.switch_to.window(browser.window_handles[window_numb-1])
        browser.get(href)

        closeAd(browser)##############

        apkName = browser.find_element(By.XPATH, '//*[contains(@class, "title_link")]/h1').text
        company = browser.find_element(By.XPATH, '//*[@class="details_sdk"]/span[@class="developer"]/a').text
        packageName = browser.find_element(By.XPATH, '/html/body/main').get_attribute("data-pkg")
        print("--------------- apk detail name:", apkName, " company:", company, " packageName:", packageName)
        if packageName in dic_package:
            print("already download package:", packageName)
            continue
        else:
            dic_package[packageName] = False

        js_code = 'window.scrollBy(0, 800)'  # 滑动指定距离
        # js_code = 'window.scrollBy(0, document.body.scrollHeight)'  # 滑动到底
        browser.execute_script(script=js_code)
        # browser.execute_script("arguments[0].scrollIntoView();", downloadBtn)
        print("--------------- scroll800")
# 更多版本
        try:
#         if True:
            # try关闭广告
            closeAd(browser)  ##############

            # 有更多版本
            allVersionBtn = browser.find_element(By.XPATH, '//a[@class="more-version"]')
            print("allVersionBtn:", allVersionBtn)
            allVersionBtn.click()
            print("--------------- allVersion")

            # try关闭广告
            closeAd(browser)  ############## 必须有

            showMoreBtn = browser.find_element(By.XPATH, '//div[@class="ver_show_more"]')
            print("showMoreBtn:", showMoreBtn)
            showMoreBtn.click() # 有时候点击没有反应
            print("--------------- showMore")

            #/html/body/div[3]/div[1]/div[4]/ul/li[21]/div
            showLessBtn = browser.find_element(By.XPATH, '//div[@class="ver_show_more"]')
            browser.execute_script("arguments[0].scrollIntoView();", showLessBtn)

            lastBtnXpath = '//div[@class="ver_content_box"]/ul/li[@class="ver_item_state"][last()]'  # 有"更多版本"
            downloadBtn = browser.find_element(By.XPATH, lastBtnXpath)  # 最后一个download按钮
            print("have show more button", downloadBtn)
        except Exception as e:
            try:
                print("except show more button,try last button", downloadBtn)
                lastBtnXpath = '//ul/li[last()]/a/div[@role="button"]'  # 没有"更多版本",多个下载
                downloadBtn = browser.find_element(By.XPATH, lastBtnXpath)
            except:
                try:
                    print("only one download button", downloadBtn)
                    lastBtnXpath = '//div/a/span[@class="download old_versions_download"]'# 只有一个下载
                    downloadBtn = browser.find_element(By.XPATH, lastBtnXpath)  # 最后一个download按钮
                except:
                    print("only one download button", downloadBtn)
                    lastBtnXpath = '//div[@class="old-versions  google-anno-skip   "]/div/a[@class="version-item dt-old-versions-variant"]/span'  # 只有一个历史版本下载
                    downloadBtn = browser.find_element(By.XPATH, lastBtnXpath)  # 最后一个download按钮
        # finally:
        #     lastBtnXpath = '//ul/li[@class="ver_item_state"]'  # 有"更多版本"
        #     print("error no show more button")

        # try关闭广告
        closeAd(browser)  ##############
        downloadBtn = browser.find_element(By.XPATH, lastBtnXpath)#最后一个download按钮
        print("lastBtnXpath:", lastBtnXpath, " downloadBtn:", downloadBtn)

        #这个可能报错，不如move_to好使
        # browser.execute_script("return arguments[0].scrollIntoView();", downloadBtn)
        # downloadBtn.click()
        ActionChains(browser).move_to_element(downloadBtn).click(downloadBtn).perform()

        downloadBtns = browser.find_elements(By.XPATH, '//*[@id="version-list"]//a[@class="download-btn"]')  # 最后一个download按钮
        print("downloadBtns:", downloadBtns)
        download = downloadBtns[len(downloadBtns) - 1]
        ActionChains(browser).move_to_element(download).click(download).perform()
        dic_package[packageName] = True
        # if len(browser.window_handles) >1:
        #     browser.close()
        #     browser.switch_to.window(browser.window_handles[0])
        # time.sleep(6)
        # # 等待下载完成
        # wait = WebDriverWait(browser, 10)
        # wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='download-complete']")))

        # # 判断下载是否成功
        # file_path = os.path.join(dir, )
        # if os.path.exists(file_path):
        #     print("下载成功！")
        # else:
        #     print("下载失败！")

    with open(dbName, 'wb') as f:
        pickle.dump(dic_package, f)
        print("dic_package write ok!")

def searchApkInternal(dir):
    found = False
    for root, dirs, files in os.walk(dir, topdown=False):
        dir_dic = []
        for dir in dirs:
            dir_dic[str(dir)] = dir
        for name in files:
            print(os.path.join(root, name))
            # 判断是否为文件（排除文件夹）
            # if os.path.isfile(name):
            # 使用os.path.splitext()获取文件名和扩展名
            file_base_name, file_ext = os.path.splitext(name)
            # 打印文件名和扩展名
            suffix = file_ext[1:]
            print(f"文件名: {file_base_name}, 扩展名: {suffix}")
            # if apkName in file_base_name and "apk" == suffix:
            apkName = file_base_name
            if "apk" == suffix:
                found = True
                print("apk:", apkName, " download complete")
                if apkName in dir_dic:
                    print("apkName in dir_dic, apkName:", apkName)
                else:
                    with ZipFile(apkName, 'r') as f:
                        print("extract apk:", apkName)
                        f.extractall()

def clickDownload():
    pass

# #####searchApkInternal(apks_dir)

# TestApkpure()
searchCrawledApks(apks_dir)