from selenium.webdriver.common.by import By
from Util.Selenium_Util import Selenium_Edge
from Util.Login_Util import getImg, getXDistance
from selenium.webdriver.common.by import By
from Util.Selenium_Util import Selenium_Edge

from time import sleep
from API.Login import edge_driver

# edge_driver = Selenium_Edge()
videolist = []

def videoAction():
    '''
    播放视频行为链
    :param driver:
    :return:
    '''
    t = "-1"
    # 总时长
    duration = edge_driver.get_element_text(xpath_kind=By.CLASS_NAME, xpath="duration", timeout=10)
    while 1:
        currentTime =  edge_driver.get_element_text(xpath_kind=By.CLASS_NAME, xpath="currentTime", timeout=10)
        print("currentTime:", currentTime)
        if (currentTime >= duration):
            print("播放完毕")
            break
        # 开始答题
        if (t == currentTime):
            print("视频暂停")
            videoQuestion()
            # 继续播放
            edge_driver.click_element(xpath_kind=By.CLASS_NAME, xpath="videoArea", timeout=10)
        t = currentTime
        print("t : " + t + "  duration : " + duration)
        # 让视频下方的进度条一直出现
        js = "document.getElementsByClassName('controlsBar')[0].style.display='block'"
        edge_driver.driver.execute_script(js)
        sleep(0.5)
        # 模拟鼠标悬停
        edge_driver.hover_element(xpath_kind=By.CLASS_NAME, xpath="box-right", timeout=10)
        # 检测间隔时间
        sleep(2)
        # / *
        # *
        # * ┌─┐       ┌─┐
        # * ┌──┘ ┴───────┘ ┴──┐
        # * │                 │
        # * │       ───       │
        # * │  ─┬┘       └┬─  │
        # * │                 │
        # * │       ─┴─       │
        # * │                 │
        # * └───┐         ┌───┘
        # * │         │
        # * │         │
        # * │         │
        # * │         └──────────────┐
        # * │                        │
        # * │                        ├─┐
        # * │                        ┌─┘
        # * │                        │
        # * └─┐  ┐  ┌───────┬──┐  ┌──┘
        # * │ ─┤ ─┤       │ ─┤ ─┤
        # * └──┴──┘       └──┴──┘
        # *神兽保佑
        # *代码无BUG!
        # * /
        # 这上面的sleep一个都不能删,大二写的屎山,咱也不知道为啥,删了就容易出bug
        edge_driver.driver.execute_script(js)

def runVideo():
    '''
    播放视频
    :param driver:
    :return:
    '''
    edge_driver.get_element(xpath_kind=By.CLASS_NAME, xpath="controlsBar")
    js = "document.getElementsByClassName('controlsBar')[0].style.display='block'"
    edge_driver.driver.execute_script(js)

    js = "var videos = document.querySelectorAll('video, audio');for(var i=0; i<videos.length; i++){videos[i].muted = true;}"
    edge_driver.driver.execute_script(js)
    # 查找倍速
    edge_driver.click_element(xpath_kind=By.CLASS_NAME, xpath="speedBox", timeout=10)
    edge_driver.get_element(xpath_kind=By.CLASS_NAME, xpath="controlsBar")
    edge_driver.driver.execute_script(js)
    # 点击1.5倍速
    edge_driver.click_element(xpath_kind=By.CLASS_NAME, xpath="speedTab.speedTab15", timeout=10)
    # 再点击播放
    edge_driver.click_element(xpath_kind=By.CLASS_NAME, xpath="videoArea", timeout=10)
    # # 进入播放系统
    # self.videoAction(driver)

def videoQuestion():
    '''
    回答视频途中出现的问题
    :param driver:
    :return:
    '''
    # 开始答题
    right_list = edge_driver.get_elements(xpath_kind=By.CLASS_NAME,xpath= "topic-item")
    try:
        for j, i in enumerate(right_list):
            if j == 0:
                print("答题弹出")
                print("开始答题")
            right_class = "iconfont.iconzhengque1"
            print("查找正确标签")
            if (edge_driver.get_element(xpath_kind=By.CLASS_NAME, xpath=right_class)):
                print("当前答题正确")
                print("答题结束")
                break
            error_class = 'iconfont.iconcuowu1'
            print("查找错误标签")
            if (edge_driver.get_element(xpath_kind=By.CLASS_NAME, xpath=error_class)):
                print("当前答题错误")
            i.click()
            sleep(2)
    except Exception:
        pass
    try:
        edge_driver.click_element("//*[@id='playTopic-dialog']/div/div[3]/span/div")
    except Exception:
        pass

def videoPageInit():
    '''
    视频页面跳转初始化操作,关闭答题界面、广告
    :param driver:
    :return:
    '''

    # 检验刚进页面是否跳转答题
    if edge_driver.get_element("//*[@id='playTopic-dialog']/div/div[3]/span/div"):
        videoQuestion()

    # 关闭弹窗
    edge_driver.click_element(xpath_kind=By.CLASS_NAME, xpath="iconfont.iconguanbi")

def videolistThread(percent_elements, numlist):
    '''
    检查在numlist区间视频列表是否观看，初始化videolist
    :param percent_elements: numlist区间的视频元素
    :param numlist: 区间
    :return:
    '''
    t = numlist[0]
    global videolist  # 在这里声明为全局变量
    for percent_element in percent_elements:
        video_text = edge_driver.get_element_text(xpath_kind=By.CLASS_NAME, xpath="catalogue_title", father_element=percent_element, timeout=10)
        if edge_driver.get_element(father_element=percent_element, xpath_kind=By.CSS_SELECTOR, xpath="b.fl.time_icofinish"):
            video = {
                'index': t,
                'topic': video_text,
                'isStudies': 1
            }
            videolist.append(video)
            print(video_text + "已经观看完毕")
        else:
            video = {
                'index': t,
                'topic': video_text,
                'isStudies': 0
            }
            videolist.append(video)
            print(video_text + "未观看完毕")
        # print(video)
        t = t + 1

# 爬取章节名称
def videolistInit():
    '''
    多线程获取所有视频名称与是否观看完毕
    :param driver:
    :param db_mysql:
    :return:
    '''
    percent_elements = edge_driver.get_elements(xpath_kind=By.CLASS_NAME, xpath="clearfix.video")
    n = len(percent_elements)
    # print("n : " + str(n))
    threadcount = 10
    from Util.Login_Util import seprateNum
    numlist = seprateNum(n, threadcount)
    global videolist
    # 重置数组
    videolist = []
    threads = []
    for i in numlist[0:len(numlist)]:
        # print(i[0], i[1])
        import threading
        split_elements = percent_elements[i[0]:i[1]]
        t = threading.Thread(target=videolistThread, args=(split_elements, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    # video_list根据index排序
    # print("videolist")
    # videolist = db_mysql.selectAll()
    videolist.sort(key=lambda x: x['index'])

def watch_video(class_index):
    from API.Login import edge_driver
    # 刷习惯分的选项
    from Util.File_Util import loading_setting
    is_auto_next = loading_setting("is_auto_next")
    # 抛出异常，用户有可能重新点击，同时有另外的接口需要接入
    edge_driver.switch_to_window_by_index(0)
    try:
        class_list_element = edge_driver.get_elements(xpath_kind=By.CLASS_NAME, xpath='dd-in', timeout=10)
        edge_driver.click(class_list_element[class_index])
    except Exception:
        pass
    videoPageInit()
    videolistInit()
    video_elements = edge_driver.get_elements(xpath_kind=By.CLASS_NAME, xpath="clearfix.video")
    print("视频数量 : " + str(len(video_elements)))
    max_video = 4
    for (index, item) in enumerate(video_elements):
        print("当前观看视频索引:" + str(index))
        topic = videolist[index]["topic"]
        if videolist[index]["isStudies"] == int(1):
            print(topic + "已经观看完毕")
            continue
        # 点击当前需要看的界面
        print("当前观看网课名称:" + topic)
        item.click()
        # 进入页面初始化
        videoPageInit()
        runVideo()
        # 进入播放系统
        videoAction()
        sleep(1)
        max_video = max_video - 1
        print(max_video)
        if is_auto_next == False and max_video <= 0:
            print("您已开启习惯分选项，已观看5个视频")
            break
    print("视频全部播放完毕")


