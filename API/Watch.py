import threading
import queue
import time
from selenium.webdriver.common.by import By

# 创建队列和事件对象
captcha_queue = queue.Queue()
stop_event = threading.Event()
condition = threading.Condition()  # 创建条件变量

# 全局线程变量
main_thread = None
captcha_thread = None

def main_task(class_index):
    from API.Login import edge_driver
    from Util.Watch_Util import watch_video
    from Util.CodeVerify_Util import _verify_code
    watch_video(class_index)
    while not stop_event.is_set():
        with condition:
            condition.wait(timeout=5)
            if not captcha_queue.empty():
                captcha = captcha_queue.get()
                if captcha == "captcha_detected":
                    print("验证码出现，处理验证码...")
                    _verify_code()
                    print("验证码处理完成，刷新页面...")
                    edge_driver.refresh()
                    watch_video(class_index)

def monitor_captcha():
    from API.Login import edge_driver
    print("验证码监测线程开启，等待验证码出现...")
    while not stop_event.is_set():
        yidun_bg_img_element = edge_driver.get_element(xpath_kind=By.CLASS_NAME, xpath='yidun_bg-img')
        if yidun_bg_img_element:
            captcha_queue.put("captcha_detected")
            with condition:
                condition.notify()

def destroy_threading():
    try:
        global main_thread, captcha_thread
        stop_event.set()
        main_thread.join()
        captcha_thread.join()
        print("所有线程已经被安全地结束。")
    except Exception as e:
        print(e)

def _watch_video(class_index):
    global main_thread, captcha_thread
    main_thread = threading.Thread(target=main_task, args=(class_index,))
    captcha_thread = threading.Thread(target=monitor_captcha)
    main_thread.start()
    captcha_thread.start()



