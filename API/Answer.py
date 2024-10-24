from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from Util.Selenium_Util import Selenium_Edge
from Util.AnswerCrawl_Util import AnswerCrawl
from Util.AnswerQuery_Util import AnswerQuery,Ocr
from Util.Watch_Util import videoPageInit
from time import sleep

from API.Login import edge_driver
# edge_driver = Selenium_Edge()

ocr = None
answerQuery = None

def _test_init(test_name, answer_url, mode=0):
    from Util.AnswerQuery_Util import Ocr
    from Util.AnswerCrawl_Util import AnswerCrawl
    global answerQuery, ocr
    # 爬取答案需要初始化重置，ocr不需要
    answerQuery = None
    print(f"正在爬取网课{test_name}答案中，请稍等.....")
    answer = AnswerCrawl(name=test_name, url=answer_url , mode=mode)
    answer_blocks = answer.getAnswerText()
    answerQuery = AnswerQuery(answer_blocks)
    print("答案爬取完成\n答案向量化完成.....")
    print("OCR初始化中，请稍等.....")
    ocr = Ocr()
    print("OCR初始化完成.....")

# def _dotest(class_index):
#     # 点击对应网课
#     from API.Login import edge_driver
#     edge_driver.switch_to_window_by_index(0)
#     click_index = class_index * 2 + 1
#     edge_driver.get_elements(xpath_kind=By.CLASS_NAME, xpath='course-menu-w')[click_index].click()
#     edge_driver.switch_to_window_by_index(1)
#     # edge_driver.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     # edge_driver.switch_to_window_by_index(1)
#     unit_test_button_elements = edge_driver.get_elements(xpath_kind=By.CLASS_NAME, xpath='themeBg', timeout=5)
#     print(f"初始测验长度: {len(unit_test_button_elements)}")
#     # 记录当前索引
#     current_index = 0
#     # 不能用for循环，防止只获取到未加载好的元素
#     while current_index < len(unit_test_button_elements):
#         edge_driver.switch_to_window_by_index(1)
#         print(f"当前索引: {current_index}")
#         # 重新获取元素以确保最新状态
#         unit_test_elements = edge_driver.get_elements(xpath_kind=By.CLASS_NAME, xpath='themeBg', timeout=5)
#         # print(unit_test_button_elements)
#         print(f"重新获取的测验长度: {len(unit_test_elements)}")
#         if current_index < len(unit_test_elements):
#             union_test = unit_test_elements[current_index]
#             print("union_test:", union_test)
#             # 点击之前滚动到元素
#             union_test.click()
#             edge_driver.switch_to_window_by_index(2)
#             # TestPage()
#             sleep(2)
#             edge_driver.driver.close()
#             # 增加索引以处理下一个元素
#             current_index += 1
#         else:
#             print(f"索引 {current_index} 超出范围，当前元素数量: {len(unit_test_button_elements)}")
#             break

def _dotest(class_index):
    from API.Login import edge_driver
    try:
        class_list_element = edge_driver.get_elements(xpath_kind=By.CLASS_NAME, xpath='dd-in')
        edge_driver.click(class_list_element[class_index])
    except Exception:
        pass
    videoPageInit()
    # unfinished_test_elements[0].click()
    edge_driver.switch_to_window_by_index(0)
    unfinished_test_elements = edge_driver.get_elements(
        xpath_kind=By.CLASS_NAME, xpath='iconfont.iconbaizhoumoshi-zhangceshi-shubiaoyiru', timeout=5)
    # 获取所有窗口句柄
    original_window = edge_driver.driver.current_window_handle
    for index, unfinished_test in enumerate(unfinished_test_elements):
        edge_driver.driver.switch_to.window(original_window)
        sleep(1)
        unfinished_test.click()
        sleep(1)
        edge_driver.switch_to_window_by_index(1)
        TestPage()
        edge_driver.driver.close()
        sleep(1)



def TestPage():
    global answerQuery,ocr
    sleep(1)
    topic_list = edge_driver.get_elements(xpath_kind=By.CLASS_NAME, xpath="subject_describe.dynamic-fonts", timeout=5)
    subject_node_list = edge_driver.get_elements(xpath_kind=By.CLASS_NAME, xpath="subject_node", timeout=5)
    for (index,topic) in enumerate(topic_list):
        sleep(0.5)
        try:
            topic_img_data = topic.screenshot_as_png
        except WebDriverException:
            sleep(0.5)
            topic_img_data = topic.screenshot_as_png
        out_text = ocr.ocr_img(topic_img_data)
        answer_list = answerQuery.get_answer(out_text)
        print("搜索到的答案:",answer_list)
        nodeLab_list = edge_driver.get_elements(father_element=subject_node_list[index], xpath_kind=By.XPATH, xpath="div")
        is_click = False
        def click_nodeLab(nodeLab_list):
            nonlocal is_click
            for nodeLab in nodeLab_list:
                try:
                    text = edge_driver.get_text(nodeLab)
                except AttributeError:
                    option_img_data = nodeLab.screenshot_as_png
                    text = ocr.ocr_img(option_img_data)
                for answer in answer_list:
                    if answer in text:
                        edge_driver.click(nodeLab)
                        print("匹配成功:",text)
                        is_click = True
        click_nodeLab(nodeLab_list)
        if is_click == False:
            print("未匹配成功!已重新规划,为您寻找第2相似的答案,")
            answer_list = answerQuery.get_answer(out_text, answer_index=1)
            click_nodeLab(nodeLab_list)
        edge_driver.click_element('//*[@id="app"]/div/div[2]/div[2]/div[3]/button[2]')
        sleep(0.9)





