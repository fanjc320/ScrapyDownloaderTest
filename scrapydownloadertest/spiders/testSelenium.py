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


def TestApkpure():
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    option.add_argument("disable-popup-blocking")
    browser = webdriver.Chrome(options=option)
    browser.get(r'https://apkpure.com/game_casual')
    print("TestApkpure")
    # latestGames = self.browser.find_elements(By.XPATH, '//main/div[5]/div[2]/div[1]/div/div/ul/li[@class="grid-col"]//div[@class="grid-row"]')
    # latestGames = browser.find_elements(By.XPATH,'//main/div[5]/div[2]/div[1]/div/div/ul/li/div/a[contains(@class, "apk-grid-button")]')
    browser.implicitly_wait(4)
    latestGames = browser.find_elements(By.XPATH,'/html/body/main/div[5]/div[2]/div[1]/div/div/ul/li/div/a[1]')
    # latestGames = browser.find_elements_by_xpath(By.XPATH,'//main/div[5]/div[2]/div[1]/div/div/ul/li/div/a[contains(@class, "apk-grid-button")]')
    print("latestGame:", latestGames)

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
        item = latestGames[i]
        # 判断元素是否可以点击
        # answer = item.is_enabled()
        print(f'item:{i}:\t{item} latestGames:{latestGames}')
        # item.screenshot("item.png")
        # ActionChains(browser).move_to_element(item).click().perform() #has no size and location
        browser.implicitly_wait(4)
        item.click()
        # latestGames[i].click()
        print("--------------- apk detail")

        #用来去除广告
        # browser.implicitly_wait(2)
        # browser.send_keys(Keys.F12)
        # browser.send_keys(Keys.F12)
        # print("--------------- F12")

        # try:
        browser.implicitly_wait(4)
        xf = browser.find_element(By.XPATH, '//*[@id="aswift_2"]')
        print(">>>>>xf:", xf)

        browser.switch_to.default_content()
        browser.switch_to.frame(xf)

        # xf_src = xf.get_attribute("src")
        # print("xf_src:", xf_src)

        # alert = browser.switch_to.alert  # 由主窗口切换到alert,返回一个alert对象
        # # time.sleep(2)
        # print("alert.text:", alert.text)
        # # alert.dismiss()  # 点击确定
        # # time.sleep(2)

        browser.implicitly_wait(4)
        body = browser.find_element(By.XPATH, '/html/body//*[@id="ad_iframe"]')  # ok
        # if body:
        #     print("body:", body)
        #     print("body.text:", body.text)#body.text: Ad
        #     print("body.html:", body.get_attribute("outerHTML"))
        #     body.click()
        # else:
        #     print("--------------- dismiss111 no found")

        browser.switch_to.frame(body)

        dismissBtn = browser.find_element(By.XPATH, '//*[@id="dismiss-button"]')
        if dismissBtn:
            print("dismissBtn:", dismissBtn)
            dismissBtn.click()
        else:
            print("--------------- dismiss no found")


        # except:
        # print("--------------- dismiss no found !!!")
        # print(browser.page_source)
        # browser.refresh()

        browser.switch_to.default_content()

        js_code = 'window.scrollBy(0, 800)'  # 滑动指定距离
        # js_code = 'window.scrollBy(0, document.body.scrollHeight)'  # 滑动到底
        browser.execute_script(script=js_code)
        print("--------------- scroll800")

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

        lastBtnXpath = '//ul/li[last()-1]/a/div[@class="ver_download_btn"]'
        downloadBtn = browser.find_element(By.XPATH, lastBtnXpath)#最后一个download按钮
        print("downloadBtn:", downloadBtn)
        downloadBtn.click()

        # labelLastBtn = browser.find_element(By.XPATH, lastBtnXpath)
        browser.execute_script("arguments[0].scrollIntoView();", downloadBtn)

        downloadBtns = browser.find_elements(By.XPATH, '//*[@id="version-list"]//a[@class="download-btn"]')  # 最后一个download按钮
        print("downloadBtns:", downloadBtns)
        downloadBtns[len(downloadBtns) - 1].click()
        i+=1

        time.sleep(6)

def clickDownload():
    pass

# print(">>>>>>>>>>")
TestApkpure()