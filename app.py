from json import JSONDecodeError

import webview
import sys
import json
from selenium.webdriver.common.by import By
from Util.Selenium_Util import Selenium_Edge
from Util.Settings import user_info_list, user_info_path, config_info_path, memory_info_path
from Util.File_Util import update_json_by_index,update_json
from Util.Stdout_Util import StdoutRedirector, log_path
import os

global edge_driver
window = None

class Api:
    def __init__(self):
        self.ensure_environment_ready()

    def ensure_environment_ready(self):
        img_folder_path = "./img"
        log_folder_path = "./Log"
        if not os.path.exists(log_folder_path):
            os.makedirs(log_folder_path)
        if not os.path.exists(img_folder_path):
            os.makedirs(img_folder_path)

    def get_log_content(self):
        return StdoutRedirector.read_log_file()

    def update_userinfo(self, data):
        print(f"正在更新用户信息于 {user_info_path}")
        update_json(user_info_path, data,)
        # 在这里处理数据，比如保存到数据库或进行其他处理
        return "用户信息保存成功"

    def update_userinfo_by_index(self, data, index):
        print(f"正在更新用户信息于 {user_info_path}")
        update_json_by_index(user_info_path, data, index)
        # 在这里处理数据，比如保存到数据库或进行其他处理
        return "用户信息保存成功"

    def update_config_info(self, data):
        # import inspect
        # # 获取当前函数的调用者信息
        # caller = inspect.stack()[1]  # stack()[0]
        # print(f"被 {caller.function} 调用")
        print(f"正在更新配置信息于 {config_info_path}")
        update_json(config_info_path, data)
        return "配置信息保存成功"

    def update_memory_info(self, data):
        print(f"正在更新记忆信息于 {memory_info_path}")
        update_json(memory_info_path, data)
        # 在这里处理数据，比如保存到数据库或进行其他处理
        return "记忆信息保存成功"

    def login(self, account, password, update=False):
        from API.Login import _login
        _login(account, password, update)

    def get_classinfo_list(self, user_info, user_index):
        from API.Login import _get_classinfo_list
        course_info_list = _get_classinfo_list()
        user_info["class_info"] = course_info_list
        self.update_userinfo_by_index(user_info, user_index)
        return "课程信息爬取成功"

    def watch_video(self, class_index):
        try:
            from API.Watch import _watch_video
            _watch_video(class_index)
        except JSONDecodeError:
            from API.Login import edge_driver
            edge_driver.destory()
        except AttributeError:
            print("发生错误，可能是浏览器驱动未正确关闭")

    def do_test(self, course_name, class_index, answer_url):
        from API.Answer import _test_init, _dotest
        _test_init(course_name, answer_url)
        _dotest(class_index)

    def open_page(self, question, url):
        last_window = webview.windows[len(webview.windows)-1]  # 假设主窗口是列表中的第一个窗口
        x, y, width, height = last_window.x, last_window.y, last_window.width, last_window.height
        # 计算新窗口的位置
        new_x = x + 50  # 新窗口在原窗口右下方
        new_y = y + 50
        # 创建新窗口并指定位置和尺寸
        webview.create_window(question, url, x=new_x, y=new_y)

    def check_update(self):
        from API.Update import _check_update
        version = _check_update()
        return "当前版本为" + version + "请点击左侧头像查看仓库地址以下载最新安装包"

    def close_browser(self):
        from API.Login import edge_driver
        if edge_driver:
            edge_driver.destory()  # 关闭浏览器并结束所有关联的驱动进程
            print("浏览器驱动已关闭")

if __name__ == '__main__':
    api = Api()
    sys.stdout = StdoutRedirector(log_path)
    dev = False
    if dev:
        window = webview.create_window('Lazy Change World v2.1.1', 'dev_index.html', js_api=api)
    else:
        window = webview.create_window('Lazy Change World v2.1.1', 'index.html', js_api=api)
    try:
        # webview.start(gui='edge', debug=True)
        webview.start(gui='edge')
    finally:
        api.close_browser()  # 确保无论如何都关闭浏览器
