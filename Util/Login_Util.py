import requests
from cv2 import imread,Canny,cvtColor,imwrite,rectangle,COLOR_GRAY2RGB,minMaxLoc,matchTemplate,TM_CCOEFF_NORMED

def getImg(url, name):
    '''
    向图片所在url获取图片到本地
    :param url:
    :param name:
    :return:
    '''
    content = requests.get(url=url).content
    with open(name, 'wb') as fp:
        fp.write(content)
        print("获取验证码图片成功")

def getXDistance(bgimg_name, brokenimg_name):
    '''
    获取验证滑块与缺口距离
    :param bgimg_name:
    :param brokenimg_name:
    :return:
    '''
    bg_img = imread(bgimg_name)  # 背景图片
    tp_img = imread(brokenimg_name)  # 缺口图片
    bg_edge = Canny(bg_img, 100, 200)
    tp_edge = Canny(tp_img, 100, 200)
    bg_pic = cvtColor(bg_edge, COLOR_GRAY2RGB)
    tp_pic = cvtColor(tp_edge, COLOR_GRAY2RGB)
    imwrite("./img/black_bgimg.jpg", bg_pic)
    imwrite("./img/black_tpimg.jpg", tp_pic)
    res = matchTemplate(bg_pic, tp_pic, TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = minMaxLoc(res)  # 寻找最优匹配
    X = max_loc[0]
    th, tw = tp_pic.shape[:2]
    tl = max_loc  # 左上角点的坐标
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
    rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
    imwrite('./img/out.jpg', bg_img)  # 保存在本地
    return X

def seprateNum(N, threadcount):
    '''
    划分线程区间
    :param N:
    :param threadcount:
    :return:
    '''
    # 对整个数字空间N进行分段CPU_COUNT
    selist = []
    n = int(N / threadcount) + 1;
    for i in range(threadcount - 1):
        right = N
        N = N - n
        if (N < 0):
            N = 0
        left = N
        s = (left, right)
        selist.append(s)
    right = N
    left = 0
    s = (left, right)
    selist.append(s)
    return selist
