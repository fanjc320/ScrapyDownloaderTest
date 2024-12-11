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

def Test2345():
    driver = webdriver.Chrome()
    driver.get("https://apkpure.com/game_casual")
    button = driver.find_element(By.ID, "button-id")
    driver.switchTo().frame("city_set_ifr");
    province = driver.findElement(By.id("province"));
    province.click();
    driver.quit();

def searchAssembly(lib_path):
    foundAssembly = 0
    # print("lib_path:", lib_path)
    for r, d, f in os.walk(lib_path):
        print("lib so filename:", f)
        for so in f:
            if "libil2cpp" in so:
                print("found Assembly.so")
                foundAssembly = 1
                break
            elif "libmono" in so:
                print("found libil2cpp.so")
                foundAssembly = 2
                break
            elif "libunity" in so:
                print("found libmain.so")
                foundAssembly = 3
                break
            # else:
            #     print("found no unity")
            if "lua" in so:
                print("found lua")
                foundAssembly *= 10
                break

def searchCrawledApks(dir):
    foundAssembly = False
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            rootName = os.path.join(root, name)
            print("rootName:", rootName)
            # 判断是否为文件（排除文件夹）
            # if os.path.isfile(name):
            # 使用os.path.splitext()获取文件名和扩展名
            file_base_name, file_ext = os.path.splitext(name)
            # 打印文件名和扩展名
            suffix = file_ext[1:]
            print(f"文件名: {file_base_name}, 扩展名:{suffix}")
            if "apk" == suffix:
                found = True
                print("apkName:", rootName)
                with ZipFile(rootName, 'r') as f:
                    print("extract name:", rootName)
                    output_folder = os.path.join(dir, file_base_name)
                    os.makedirs(output_folder, exist_ok=True)
                    f.extractall(output_folder + "")

                    lib_path1 = os.path.join(output_folder, "lib\\armeabi-v7a")
                    lib_path2 = os.path.join(output_folder, "lib\\arm64-v8a")
                    lib_path3 = os.path.join(output_folder, "lib\\x86")
                    if os.path.exists(lib_path1):
                        lib_path = lib_path1
                    elif os.path.exists(lib_path2):
                        lib_path = lib_path2
                    elif os.path.exists(lib_path3):
                        lib_path = lib_path3

                    res = searchAssembly(lib_path)
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
                        print("dismissBtn:", dismissBtn)
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


apks_dir = r"E:\crawl_apks"
def TestApkpure():
    option = webdriver.ChromeOptions()

    prefs = {
        "download.default_directory": apks_dir,
        "profile.default_content_setting_values.automatic_downloads": 1,  # 允许多文件下载
        # 无用 "debuggerAddress": "127.0.0.1:62271" #只打开一个浏览器实例 chrome所在路劲\chrome.exe --remote-debugging-port=12306 https://blog.csdn.net/Qwertyuiop2016/article/details/103488817
    }
    # for root, dirs, files in os.walk(dir, topdown=False):
    #     for name in files:
    #         print(os.path.join(root, name))
    #         # 判断是否为文件（排除文件夹）
    #         # if os.path.isfile(name):
    #             # 使用os.path.splitext()获取文件名和扩展名
    #         file_base_name, file_ext = os.path.splitext(name)
    #         # 打印文件名和扩展名
    #         print(f"文件名: {file_base_name}, 扩展名: {file_ext[1:]}")
    #     for name in dirs:
    #         print(os.path.join(root, name))

    option.add_experimental_option("prefs", prefs)
    option.add_experimental_option("detach", True)
    option.add_argument("disable-popup-blocking")
    # option.add_experimental_option("debuggerAddress", "127.0.0.1:12306")
    browser = webdriver.Chrome(options=option)

    # try:
    #     browser.get("http://www.google.com")
    #     input_element = browser.find_element_by_name("q")
    #     input_element.send_keys("fuck you")
    #     input_element.submit()
    #     link = browser.find_element_by_xpath(
    #         '//*[@id="rso"]/div[1]/div/div[2]/div/div/h3/a').click()
    #     #     for windows change command to control.
    #     ActionChains(browser).move_to_element(link).key_down(Keys.COMMAND).click(link).key_up(Keys.COMMAND).perform()
    #     time.sleep(5)
    # except Exception as e:
    #     print(e)
    #     browser.close()
    #
    # return

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

    count = 1
    for i in range(len(latestGames)):
        if count > 5:
            break
        count += 1
        # browser.implicitly_wait(5)
        browser.switch_to.window(browser.window_handles[0])
        item = latestGames[i]

        href = item.get_attribute("href")
        # 判断元素是否可以点击
        # answer = item.is_enabled()
        print("href:", href)
        print(f'item:{i}:\t{item} latestGames:{latestGames}')

        # item.screenshot("item.png")

        # action = ActionChains(browser)
        # action.key_down(Keys.CONTROL).click(item).key_up(Keys.CONTROL).perform()
        # ActionChains(browser).key_down(Keys.CONTROL).click(item).key_up(Keys.CONTROL).perform()
        # action.key_down(Keys.CONTROL).perform()
        # ActionChains(browser).key_down(Keys.CONTROL).click(item).key_up(Keys.CONTROL).perform()
        # item.click()
        # action.key_up(Keys.CONTROL).perform()
        # ActionChains(browser).move_to_element(item).key_down(Keys.CONTROL).click(item).key_up(Keys.CONTROL).perform()

        browser.execute_script("window.open('');")
        window_numb = len(browser.window_handles)
        browser.switch_to.window(browser.window_handles[window_numb-1])
        browser.get(href)
        # print("go to new window_handle after sleep num:", window_numb)
        # if window_numb > 1:
        #     browser.switch_to.window(browser.window_handles[window_numb-1])

        closeAd(browser)##############
        # return

        apkName = browser.find_element(By.XPATH, '//*[@class="title_link no-rating"]/h1').text
        company = browser.find_element(By.XPATH, '//*[@class="details_sdk"]/span[@class="developer"]/a').text
        print("--------------- apk detail name:", apkName, " company:", company)

        js_code = 'window.scrollBy(0, 800)'  # 滑动指定距离
        # js_code = 'window.scrollBy(0, document.body.scrollHeight)'  # 滑动到底
        browser.execute_script(script=js_code)
        # browser.execute_script("arguments[0].scrollIntoView();", downloadBtn)
        print("--------------- scroll800")
        # continue
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

        # lastBtnXpath = '//ul/li/a[@class="ver_download_link"]/div[@class="ver_download_btn"]'
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
        downloadBtns[len(downloadBtns) - 1].click()

        i+=1
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
        print("checked apk:", apkName, " company:", company)


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

# print(">>>>>>>>>>")
TestApkpure()
# #####searchApkInternal(apks_dir)
# searchCrawledApks(apks_dir)