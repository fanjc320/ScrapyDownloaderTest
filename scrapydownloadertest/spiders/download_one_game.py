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
    # dic_all_crawled_apks = getAllCrawledApks(apks_dir)
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

    # browser.get(r'https://apkpure.com/melon-maker-fruit-game/com.superbox.aos.suikagame/versions') # ok
    browser.get(r'https://apkpure.com/match-3d-blast-matching-games/com.puzzle.fun.free.matching3d')
    # print("TestApkpure window handle:", browser.current_window_handle)

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

    closeAd(browser)##############

    js_code = 'window.scrollBy(0, 800)'  # 滑动指定距离
    # js_code = 'window.scrollBy(0, document.body.scrollHeight)'  # 滑动到底
    browser.execute_script(script=js_code)
    # browser.execute_script("arguments[0].scrollIntoView();", downloadBtn)
#     print("--------------- scroll800")
    try:
        # 有更多版本  视情况选择是否打开/注释代码
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
    except Exception as e:
        print("except show more button, err")

#     # try关闭广告
    closeAd(browser)  ##############

    downloadBtns = browser.find_elements(By.XPATH, '//ul/li/a[@class="ver_download_link"]')
    apkNumb = 0
    for downloadApk in downloadBtns:
        browser.switch_to.window(browser.window_handles[0])

        href = downloadApk.get_attribute("href")
        print("href:", href)
        browser.execute_script("window.open('');")
        window_numb = len(browser.window_handles)
        browser.switch_to.window(browser.window_handles[window_numb-1])
        browser.get(href)

        downloadBtn = browser.find_element(By.XPATH, '//div/a[contains(@class, "downloading-btn")]')
        ActionChains(browser).move_to_element(downloadBtn).click(downloadBtn).perform()

        apkNumb += 1

    print("apkNumb:", apkNumb)

TestApkpure()


