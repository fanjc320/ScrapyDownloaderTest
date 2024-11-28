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
    for r, d, f in os.walk(lib_path):
        print("lib so filename:", f)
        if "Assembly" in f:
            print("found Assembly.so")
            foundAssembly = 1
        elif "libil2cpp" in f:
            print("found libil2cpp.so")
            foundAssembly = 2
        elif "libunity" in f:
            print("found libmain.so")
            foundAssembly = 3
        else:
            print("found no unity")
def TestApkpure():
    option = webdriver.ChromeOptions()
    dir = r"E:\apks"
    prefs = {
        "download.default_directory": dir,
        "profile.default_content_setting_values.automatic_downloads": 1  # 允许多文件下载
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

    foundAssembly = False
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            rootName = os.path.join(root, name)
            print(rootName)
            # 判断是否为文件（排除文件夹）
            # if os.path.isfile(name):
            # 使用os.path.splitext()获取文件名和扩展名
            file_base_name, file_ext = os.path.splitext(name)
            # 打印文件名和扩展名
            suffix = file_ext[1:]
            print(f"文件名: {file_base_name}, 扩展名:{suffix}")
            if "apk" == suffix:
                found = True
                print("apk name:", rootName)
                with ZipFile(rootName, 'r') as f:
                    print("extract name:", rootName)
                    output_folder = os.path.join(dir, file_base_name)
                    os.makedirs(output_folder, exist_ok=True)
                    f.extractall(output_folder + "")

                    lib_path1 = os.path.join(output_folder, "./lib/armeabi-v7a")
                    lib_path2 = os.path.join(output_folder, "./lib/arm64-v8a")
                    if os.path.exists(lib_path1):
                        lib_path = lib_path1
                    elif os.path.exists(lib_path2):
                        lib_path = lib_path2

                    res = searchAssembly(lib_path)


    # prefs = {"download.default_directory": "../apks"}
    option.add_experimental_option("prefs", prefs)
    option.add_experimental_option("detach", True)
    option.add_argument("disable-popup-blocking")
    browser = webdriver.Chrome(options=option)
    browser.get(r'https://apkpure.com/game_casual')
    print("TestApkpure window handle:")
    print(browser.current_window_handle)
    # latestGames = self.browser.find_elements(By.XPATH, '//main/div[5]/div[2]/div[1]/div/div/ul/li[@class="grid-col"]//div[@class="grid-row"]')
    # latestGames = browser.find_elements(By.XPATH,'//main/div[5]/div[2]/div[1]/div/div/ul/li/div/a[contains(@class, "apk-grid-button")]')
    browser.implicitly_wait(4)

    latestGames = browser.find_elements(By.XPATH,'/html/body/main/div[5]/div[2]/div[1]/div/div/ul/li/div/a[1]')
    # latestGames = browser.find_elements_by_xpath(By.XPATH,'//main/div[5]/div[2]/div[1]/div/div/ul/li/div/a[contains(@class, "apk-grid-button")]')
    print("latestGames:", latestGames)

    try:
        element = WebDriverWait(browser, 10).until(
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
        if count > 1:
            break
        ++count
        # browser.implicitly_wait(5)
        time.sleep(3)
        # browser.execute_script('window.open("http://news.baidu.com/")')

        item = latestGames[i]
        # 判断元素是否可以点击
        # answer = item.is_enabled()
        print(f'item:{i}:\t{item} latestGames:{latestGames}')
        # item.screenshot("item.png")
        # ActionChains(browser).move_to_element(item).click().perform() #has no size and location
        browser.implicitly_wait(4)
        print("item.txt:", item.text)
        # item.send_keys(Keys.CONTROL)
        # item.click()
        action = ActionChains(browser)
        action.key_down(Keys.CONTROL).click(item).key_up(Keys.CONTROL).perform()
        if len(browser.window_handles) >1:
            print("go to new window_handle")
            browser.switch_to.window(browser.window_handles[1])
        # latestGames[i].click()
        # browser.execute_script("window.open('');")
        apkName = browser.find_element(By.XPATH, '//*[@class="title_link no-rating"]/h1').text
        company = browser.find_element(By.XPATH, '//*[@class="details_sdk"]/span[@class="developer"]/a').text
        print("--------------- apk detail name:", apkName, " company:", company)


# 弹窗广告
        try:
            browser.implicitly_wait(4)
            xf = browser.find_element(By.XPATH, '//*[@id="aswift_2"]')
            print("switch to xf:", xf)

            browser.switch_to.default_content()
            browser.switch_to.frame(xf)

            # xf_src = xf.get_attribute("src")
            # print("xf_src:", xf_src)

            browser.implicitly_wait(4)
            body = browser.find_element(By.XPATH, '/html/body//*[@id="ad_iframe"]')  # ok
            browser.switch_to.frame(body)

            dismissBtn = browser.find_element(By.XPATH, '//*[@id="dismiss-button"]')
            if dismissBtn:
                print("dismissBtn:", dismissBtn)
                dismissBtn.click()
            else:
                print("dismissBtn not found")

        except:
            print(" ad box no found !!!")
            # print(browser.page_source)
            # browser.refresh()
            browser.switch_to.default_content()

        browser.switch_to.default_content()
        js_code = 'window.scrollBy(0, 800)'  # 滑动指定距离
        # js_code = 'window.scrollBy(0, document.body.scrollHeight)'  # 滑动到底
        browser.execute_script(script=js_code)
        # browser.execute_script("arguments[0].scrollIntoView();", downloadBtn)
        print("--------------- scroll800")

# 更多版本
        try:
            # 有更多版本
            allVersionBtn = browser.find_element(By.XPATH, '//a[@class="more-version"]')
            print("allVersionBtn:", allVersionBtn)
            allVersionBtn.click()
            print("--------------- allVersion")

            showMoreBtn = browser.find_element(By.XPATH, '//div[@class="ver_show_more"]')
            print("showMoreBtn:", showMoreBtn)
            showMoreBtn.click()
            print("--------------- showMore")

            #/html/body/div[3]/div[1]/div[4]/ul/li[21]/div
            showLessBtn = browser.find_element(By.XPATH, '//div[@class="ver_show_more"]')
            browser.execute_script("arguments[0].scrollIntoView();", showLessBtn)

            lastBtnXpath = '//ul/li[@class="ver_item_state"]'  # 有"更多版本"
            print("have show more button")
            downloadBtns = browser.find_elements(By.XPATH, lastBtnXpath)  # 最后一个download按钮
            downloadBtn = downloadBtns[len(downloadBtns) - 1]
        except:
            print("except show more button")
            lastBtnXpath = '//ul/li[last()]/a/div[@role="button"]'  # 没有"更多版本"
            downloadBtn = browser.find_elements(By.XPATH, lastBtnXpath)
        else:
            lastBtnXpath = '//ul/li[@class="ver_item_state"]'  # 有"更多版本"
            print("no show more button")

        # lastBtnXpath = '//ul/li/a[@class="ver_download_link"]/div[@class="ver_download_btn"]'

        # downloadBtn = browser.find_element(By.XPATH, lastBtnXpath)#最后一个download按钮
        print("downloadBtn:", downloadBtn)
        # labelLastBtn = browser.find_element(By.XPATH, lastBtnXpath)
        browser.execute_script("arguments[0].scrollIntoView();", downloadBtn)
        downloadBtn.click()

        downloadBtns = browser.find_elements(By.XPATH, '//*[@id="version-list"]//a[@class="download-btn"]')  # 最后一个download按钮
        print("downloadBtns:", downloadBtns)
        downloadBtns[len(downloadBtns) - 1].click()

        i+=1
        if len(browser.window_handles) >1:
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
        # time.sleep(6)
        # 等待下载完成
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='download-complete']")))

        # # 判断下载是否成功
        # file_path = os.path.join(dir, )
        # if os.path.exists(file_path):
        #     print("下载成功！")
        # else:
        #     print("下载失败！")
        found = False
        for root, dirs, files in os.walk(dir, topdown=False):
            for name in files:
                print(os.path.join(root, name))
                # 判断是否为文件（排除文件夹）
                # if os.path.isfile(name):
                # 使用os.path.splitext()获取文件名和扩展名
                file_base_name, file_ext = os.path.splitext(name)
                # 打印文件名和扩展名
                suffix = file_ext[1:]
                print(f"文件名: {file_base_name}, 扩展名: {suffix}")
                if apkName in file_base_name and "apk" == suffix:
                    found = True
                    print("apk:", apkName, " company:", company, " download complete")
                    with ZipFile(apkName, 'r') as f:
                        f.extractall()



def clickDownload():
    pass

# print(">>>>>>>>>>")
TestApkpure()