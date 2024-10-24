import requests
from lxml import etree
import re

# 此工具类用于爬取不同网站的答案
class AnswerCrawl:
    def __init__(self,name="", mode=0, url=None, extend_url=None):
        '''
        :param name:网课名称
        :param mode:一级目录爬取网址选择
        :param url: 二级目录爬取网址
        :param extend_url:附加网址
        '''
        self.name = name
        self.url = url
        self.mode = mode
        self.extend_url = extend_url

    def getAnswerText(self):
        if self.mode == 0:
            return self.getAnswerText_Mode0()

    def SplitText_General(self, text):
        '''
        :param text: 所有文本
        :return: 普通模式分割文本块
        '''
        blocks = []
        current_block = []
        # 遍历每行文本
        for line in text:
            # 如果遇到空字符串且current_block不为空，表示一个完整的题目块结束
            if line == '' and current_block:
                blocks.append('\n'.join(current_block))  # 将当前块加入blocks
                current_block = []  # 重置current_block
            else:
                current_block.append(line)  # 将非空行加入当前块
        # 如果最后一个块没有被加入（文件结尾没有空字符串）
        if current_block:
            blocks.append('\n'.join(current_block))
        return blocks

    def analysisWeb(self, url):
        '''
        :param url: 网页地址
        :return:
        '''
        response = requests.get(url)
        html = response.text
        html = html.encode('iso-8859-1').decode('gbk')
        tree = etree.HTML(html)
        return tree

    def getContent_Mode0(self):
        # 匹配mode0的目录信息
        tree = self.analysisWeb('http://www.iamooc.com/zhihuishudaan.htm')
        text_node = tree.xpath(f"//font[contains(text(), \"{self.name}\")]")
        if text_node:
            href = text_node[0].xpath('../@href')[0]
            href = f"http://www.iamooc.com/{href}"
            return href
        else:
            import re
            self.name = re.sub(r'\（.*?\）', '', self.name)
            print(f"第一次答案爬取失败，正在尝试第二次爬取{self.name}答案\n")
            text_node = tree.xpath(f"//font[contains(text(), \"{self.name}\")]")
            if text_node:
                href = text_node[0].xpath('../@href')[0]
                href = f"http://www.iamooc.com/{href}"
                return href
            else :
                # 抛出异常
                raise Exception("第二次答案爬取失败，请检查网络连接或答案是否爬取完成")

    def getAnswerText_Mode0(self):
        if self.url == '' or self.url == None:
            self.url = self.getContent_Mode0()
        # 获取文本信息
        tree = self.analysisWeb(self.url)
        text = tree.xpath('/html/body/p/font[2]')
        text = text[0].xpath('text()')
        # 将所有的字符串过滤掉\r\n
        text = [re.sub(r'\r\n', '', i) for i in text]
        blocks = self.SplitText_General(text)
        return blocks

if __name__ == '__main__':
    answer = AnswerCrawl('创造性思维与创新方法（大连理工大学）')
    print(answer.getAnswerText_Mode0())
