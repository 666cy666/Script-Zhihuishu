from json import JSONDecodeError

from selenium.webdriver.common.by import By
from Util.Selenium_Util import Selenium_Edge
from Util.Login_Util import getImg, getXDistance
from selenium.webdriver.common.by import By
from Util.Selenium_Util import Selenium_Edge

edge_driver = None

def init_page(update):
    global edge_driver
    from Util.File_Util import loading_setting
    # is_auto_update = loading_setting("is_auto_update")
    is_headless = loading_setting("is_headless")
    edge_driver = Selenium_Edge(update=update, headless=is_headless)
    edge_driver.driver.set_window_size(1300, 800)  # 设置浏览器窗口大小
    edge_driver.get_driver('https://onlineweb.zhihuishu.com/onlinestuh5')

def login_page(account, password):
    global edge_driver
    edge_driver.input_text('//*[@id="lUsername"]', text=account)
    edge_driver.input_text('//*[@id="lPassword"]', text=password)
    edge_driver.click_element('//*[@id="f_sign_up"]/div[1]/span')

    yidun_bg_img_url = edge_driver.get_element_attribute(xpath_kind=By.CLASS_NAME, xpath='yidun_bg-img',
                                                         attribute="src", is_watch=True)
    yidun_broken_url = edge_driver.get_element_attribute(xpath_kind=By.CLASS_NAME, xpath='yidun_jigsaw',
                                                         attribute="src", is_watch=True)
    bg_img_name = "./img/bgimg_src.jpg"
    broken_img_name = "./img/brokenimg_src.jpg"
    getImg(yidun_bg_img_url, bg_img_name)
    getImg(yidun_broken_url, broken_img_name)
    move_x = getXDistance(bg_img_name, broken_img_name)
    print("验证码拖动的距离:" + str(move_x) + "px")
    action = edge_driver.action
    try:
        drag_element = edge_driver.get_element(xpath_kind=By.CLASS_NAME,xpath='yidun_slider.yidun_slider--hover')
        action.click_and_hold(drag_element)
        # # 第二步：相对鼠标当前位置进行移动
        action.move_by_offset(move_x + 10, 0)
        # # 第三步：释放鼠标
        action.release()
        # # 执行动作
        action.perform()
        if (edge_driver.get_element('//*[@id="titleListAll"]', timeout=3)):
            print("通过验证码，进入系统")
        else:
            print("未通过验证码，正在重新验证")
            login_page(account, password)
    except Exception as e:
        print(f"未通过验证码，请重启或手动登录, 报错信息{e}")

def _login(account,password, update):
    global edge_driver
    from Util.File_Util import loading_setting
    # is_play_more = loading_setting("is_play_more")
    # if is_play_more:
    try:
        init_page(update)
    except JSONDecodeError:
        print("抱歉，目前不允许多开账号，敬请期待下个版本")
    login_page(account, password)

def _get_classinfo_list():
    global edge_driver
    class_list = edge_driver.get_elements(xpath_kind=By.CLASS_NAME, xpath='item-left-course')
    course_info_list = []
    for class_element in class_list:
        text = edge_driver.get_text(class_element)
        # 根据\n分词
        text_list = text.split('\n')
        name = text_list[0]
        teacher = text_list[1]
        school = text_list[2]
        if school not in name:
            name = name + "（" + school + "）"
        title = {
            "course_title": name,
            "course_text": teacher
        }
        course_info_list.append(title)
    return course_info_list





