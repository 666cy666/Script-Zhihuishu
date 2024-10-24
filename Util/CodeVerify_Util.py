from cv2 import (
    imdecode, cvtColor, inRange, bitwise_not, bitwise_and,
    threshold, findContours, boundingRect, imencode, rectangle, IMREAD_COLOR,
    COLOR_RGB2BGR, COLOR_BGR2RGB, COLOR_RGB2GRAY, THRESH_BINARY, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE
)
import numpy as np
from urllib.parse import urlparse
import requests
from PIL import Image
import io
import re
import ddddocr

# result = ocr.classification(image, probability=True)
#
# 工具函数, 用于提取单个数字和字母
from selenium.webdriver.common.by import By


def extract_digits_and_letters(input_string):
    # 使用正则表达式提取所有单个数字和字母
    input_string = input_string.upper()
    pattern = r'[A-Za-z0-9]'
    matches = re.findall(pattern, input_string)
    return matches

# 工具函数, 用于比较字符位置
def compare_positions(positions, target_char, func=min):
    target_position = func(
        (item['position'] for item in positions if item['text'] == target_char),
        key=lambda pos: pos[2] * pos[3],
        default=False
    )
    if target_position:
        x, y, w, h = target_position
        center_x = x + w / 2
        center_y = y + h / 2
        # 使用传入的函数（max 或 min）来找到符合条件的最大或最小区域
        return center_x,center_y
    else:
        return False

def load_img(img_url):
    # 若 img 是网络地址
    if isinstance(img_url, str):
        parsed_url = urlparse(img_url)
        if parsed_url.scheme in ['http', 'https']:
            response = requests.get(img_url)
            if response.status_code == 200:
                image_np = np.frombuffer(response.content, np.uint8)
                return imdecode(image_np, IMREAD_COLOR)
            else:
                raise ValueError(f"无法获取图像，状态码: {response.status_code}")
        # 若 img 是本地路径（包括含有中文路径的情况）
        else:
            # 使用 PIL 打开图像，然后转换为 OpenCV 格式
            with open(img_url, 'rb') as f:
                image_pil = Image.open(io.BytesIO(f.read()))
                # 将 PIL 图像转换为 OpenCV 格式
                image_cv = cvtColor(np.array(image_pil), COLOR_RGB2BGR)
                return image_cv
    else:
        raise TypeError("输入必须是字符串类型的网络地址或本地路径")

# 工具函数, 用于字符区域检测
def find_contours(image):
    # 将图片转换为 RGB
    image_rgb = cvtColor(image, COLOR_BGR2RGB)

    # 定义背景颜色
    background_color = np.array([230, 230, 230], dtype=np.uint8)

    # 设置容差
    tolerance = 20
    lower_bound = background_color - tolerance
    upper_bound = background_color + tolerance

    # 生成掩码并反转，得到字符部分的掩码
    mask = inRange(image_rgb, lower_bound, upper_bound)
    mask_inv = bitwise_not(mask)

    # 过滤掉背景色，保留字符部分（为了显示清晰，生成灰度图）
    filtered_image = bitwise_and(image_rgb, image_rgb, mask=mask_inv)
    filtered_gray = cvtColor(filtered_image, COLOR_RGB2GRAY)

    # 使用阈值将字符变成二值图像，方便轮廓检测
    _, thresh = threshold(filtered_gray, 1, 255, THRESH_BINARY)

    # 寻找轮廓
    contours, _ = findContours(thresh, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)
    contours_extend = []
    for i, contour in enumerate(contours):
        x, y, w, h = boundingRect(contour)
        extend = 3
        x = x-extend if x-extend > 0 else x
        y = y-extend if y-extend > 0 else y
        w = w+extend*2 if x+w+extend < image_rgb.shape[1] else w
        h = h+extend*2 if y+h+extend < image_rgb.shape[0] else h
        if w > 10 and h > 10:  # 过滤掉噪点，只保留可能的字符
            # 裁剪出字符区域
            char_roi = image_rgb[y:y+h, x:x+w]
            contours_extend.append([x, y, w, h, char_roi])
    return contours

# 工具函数, 用于识别字符
def indentify_contours(image_rgb, contours, show = False):
    ocr = ddddocr.DdddOcr(show_ad=False)
    # 初始化 ddddocr 识别器
    ocr.set_ranges(6)
    def extend_contour(contour, extend = 4):
        x, y, w, h = boundingRect(contour)
        x = x-extend if x-extend > 0 else x
        y = y-extend if y-extend > 0 else y
        w = w+extend*2 if x+w+extend < image_rgb.shape[1] else w
        h = h+extend*2 if y+h+extend < image_rgb.shape[0] else h
        return [x, y, w, h]
    # 遍历轮廓，裁剪字符区域并识别
    result_list = []
    for i, contour in enumerate(contours):
        x, y, w, h = extend_contour(contour)
        if w > 10 and h > 10:  # 过滤掉噪点，只保留可能的字符
            # 裁剪出字符区域
            char_roi = image_rgb[y:y+h, x:x+w]
            # 将裁剪的字符区域转换为字节
            _, char_buffer = imencode('.png', char_roi)
            char_bytes = char_buffer.tobytes()
            # 使用 ddddocr 识别字符
            char_text_probability = ocr.classification(char_bytes, probability=True)
            s = ""
            for i in char_text_probability['probability']:
                s += char_text_probability['charsets'][i.index(max(i))]
            result = {
                'position': [x, y, w, h],
                # 强制转化为大写
                'text': s[0].upper()
            }
            result_list.append(result)
            # print(f"识别到的字符: {s}")
    if show:
        for i, contour in enumerate(contours):
            x, y, w, h = extend_contour(contour)
            # 在原图上绘制边界框并显示识别结果
            rectangle(image_rgb, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # putText(image_rgb, s, (x, y - 10), FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        # 使用 matplotlib 显示结果
        from matplotlib import pyplot as plt
        plt.imshow(image_rgb)
        plt.axis('off')  # 隐藏坐标轴
        plt.show()
    return result_list

def get_target_postion(image_path, target_text):
    # 加载图像
    image = load_img(image_path)
    # 将图像转换为 RGB 格式
    contours = find_contours(image)
    result_list = indentify_contours(image, contours)
    print(result_list)
    # 准备工作结束
    target_text = target_text.replace(".png", "")
    target_char = extract_digits_and_letters(target_text)[-1:][0]
    print("检测字符：", target_char)
    if "侧向的" in target_text:
        target_position = compare_positions(result_list, target_char)
    # 后面需要改的操作，目前是要你命3000
    else:
        target_position = compare_positions(result_list, target_char, func=max)
    return target_position

def _verify_code():
    from API.Login import edge_driver
    # 有个多次验证的按钮
    if edge_driver.get_element(xpath_kind=By.CLASS_NAME, xpath='s1', timeout=1):
        edge_driver.click_element(xpath_kind=By.CLASS_NAME, xpath='s1')
    yidun_bg_img_src = edge_driver.get_element_attribute(xpath_kind=By.CLASS_NAME, xpath='yidun_bg-img',
                                                     attribute='src')
    yidun_tips__text = edge_driver.get_element_text(xpath_kind=By.CLASS_NAME,
                                                    xpath='yidun_tips__text.yidun-fallback__tip')
    center_x, center_y = get_target_postion(yidun_bg_img_src, yidun_tips__text)
    yidun_bg_img_element = edge_driver.get_element(xpath_kind=By.CLASS_NAME, xpath='yidun_bg-img')
    # 获取验证码元素的位置和大小
    size = yidun_bg_img_element.size
    target_x = center_x - size['width'] / 2
    target_y = center_y - size['height'] / 2
    from selenium.webdriver import ActionChains
    actions = ActionChains(edge_driver.driver)
    actions.move_to_element_with_offset(yidun_bg_img_element, target_x, target_y).click().perform()
    # 再次查找
    from time import sleep
    sleep(1)
    yidun_bg_img_element = edge_driver.get_element(xpath_kind=By.CLASS_NAME, xpath='yidun_bg-img')
    if yidun_bg_img_element:
        print("验证码验证失败，重新验证")
        _verify_code()

def test():
    # 正确加载并传递图像
    image_path = '../CodeImg/侧向的大写K.png'
    target_text = '侧向的大写K.png'
    center_x, center_y = get_target_postion(image_path, target_text)
    # 打印结果
    # print(f"找到的轮廓数量: {len(contours)}")
    # print(contours)
    print(center_x, center_y )
    # contours