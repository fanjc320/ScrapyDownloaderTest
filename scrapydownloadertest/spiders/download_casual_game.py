# -*- coding: utf-8 -*-
from crawl_common import *
# def searchAssembly(lib_path):
#     foundAssembly = 0
#     # print("lib_path:", lib_path)
#     for r, d, f in os.walk(lib_path, topdown= True):
#         fileCnt = len(f)
#         print("lib so fileCount:", fileCnt, " so:", f)
#         if fileCnt == 0:
#             print("searchAssembly lib_path error!!!!!")
#         for so in f:
#             if "libil2cpp" in so:
#                 print("found libil2cpp.so")
#                 foundAssembly = 1
#                 break
#             elif "libmono" in so:
#                 print("found libmono*.so")
#                 foundAssembly = 2
#                 break
#             elif "libunity" in so:
#                 print("found libunity.so")
#                 foundAssembly = 3
#                 break
#             elif "libcocos" in so:
#                 print("found libcocos*.so")
#                 foundAssembly = 3
#                 break
#             # else:
#             #     print("found no unity")
#             if "lua" in so:
#                 print("found lua")
#                 foundAssembly *= 10
#                 break
#     return foundAssembly

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

def TestApkpure():
    dic_all_crawled_apks = getAllCrawledApks(apks_dir)
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
        company = "null"
        try:
            company = browser.find_element(By.XPATH, '//*[@class="details_sdk"]/span[@class="developer"]/a').text
        except:
            company = "except"
        packageName = browser.find_element(By.XPATH, '/html/body/main').get_attribute("data-pkg")
        print("--------------- apk detail apkName:", apkName, " company:", company, " packageName:", packageName)
        print("dic_all_crawled_apks:", dic_all_crawled_apks)
        found = False
        for apk in dic_all_crawled_apks:
            apkSub = apk[0:len(apkName)]
            seq = difflib.SequenceMatcher(lambda x: x in "-_:", apkSub, apkName)
            ratio = seq.ratio()
            # print('difflib apksub:', apkSub, 'apkName', apkName, ' similarity: ', ratio)
            if ratio > 0.9:
                found = True
                print("already download apkName:", apkName)
                break
        if found:
            continue
        # if packageName in dic_package:
        #     print("already download package:", packageName)
        #     continue
        # else:
        #     dic_package[packageName] = False

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
            downloadBtn = browser.find_element(By.XPATH, lastBtnXpath)  # 最后一个download按钮, 如果找不到会出现except
            print("have show more button", downloadBtn)
        except Exception as e:
            try:
                print("except show more button,try last button")
                lastBtnXpath = '//ul/li[last()]/a/div[@role="button"]'  # 没有"更多版本",多个下载, 如果找不到会出现except
                downloadBtn = browser.find_element(By.XPATH, lastBtnXpath)
            except:
                try:
                    print("only one download button 111")
                    lastBtnXpath = '//div/a/span[@class="download old_versions_download"]'# 只有一个下载
                    downloadBtn = browser.find_element(By.XPATH, lastBtnXpath)  # 最后一个download按钮, 如果找不到会出现except
                except:
                    print("only one download button 222")
                    lastBtnXpath = '//div[@class="old-versions  google-anno-skip   "]/div/a[@class="version-item dt-old-versions-variant"]/span'  # 只有一个历史版本下载
                    downloadBtn = browser.find_element(By.XPATH, lastBtnXpath)  # 最后一个download按钮, 如果找不到会出现except
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


TestApkpure()


