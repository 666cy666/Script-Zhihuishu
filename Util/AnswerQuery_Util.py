import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

import re

from cnocr import CnOcr
from io import BytesIO
from PIL import Image
import os
import sys
import string

# 过滤文本
def remove_punctuation(text):
    '''
    去除文本中的标点符号和空白字符
    :param text:
    :return:
    '''
    # 定义一个标点符号表，包括常见的英文和中文标点
    punctuation = string.punctuation + "。？！，、；：“”‘’（）《》【】—…－"
    # 使用正则表达式替换掉标点符号
    text_no_punctuation = re.sub(f"[{re.escape(punctuation)}]", "", text)
    # 使用正则表达式去除所有空白字符（包括空格、制表符等）
    text_no_punctuation = re.sub(r"\s+", "", text_no_punctuation)
    return text_no_punctuation

# 分割过滤答案
def split_by_punctuation(text, option_text_list):
    import re
    # 定义标点符号作为分割符
    punctuation_pattern = r"[；【】《》（）:;：#]"
    # 使用正则表达式分割文本
    segments = re.split(punctuation_pattern, text)
    # print(segments)
    segments = [segment for segment in segments if segment and "答案" not in segment]
    # 多选答案校验,若答案中存在ABCD选项则需要去选项中找答案
    for index,segment in enumerate(segments):
        verify_answer = bool(re.fullmatch(r"[ABCDE]*", segment))
        if verify_answer:
            segments = []
            for option_text in option_text_list:
                option = option_text[0]
                if option in segment:
                    # 过滤空格与选项
                    clean_option_text = remove_punctuation(option_text)
                    segments.append(clean_option_text[1:])
        # 如果选项内容包含对错标记，则也加进去
        if '对' == segment[0] or '√' in segment[0]:
            segments = ['对','√']
        if '错' == segment[0] or 'X' in segment[0]:
            segments = ['错','X','x']
    print("答案",segments)
    return segments

class AnswerQuery:
    def __init__(self, blocks):
        self.blocks = blocks
        self.tfidf_model = TfidfVectorizer()
        self.tfidf_matrix = self.VectorizeText()

    def VectorizeText(self):
        import time
        # 对每个文本块进行分词
        segmented_blocks = [" ".join(jieba.cut(block)) for block in self.blocks]
        start_time = time.time()
        # 向量化文本块
        tfidf_matrix = self.tfidf_model.fit_transform(segmented_blocks)
        end_time = time.time()
        print(f"向量化文本块耗时: {end_time - start_time}秒")
        return tfidf_matrix

    def find_similar(self, query, top_n=3):
        # 将查询分词并向量化
        query_cut = " ".join(jieba.cut(query))
        query_vec = self.tfidf_model.transform([query_cut])
        # 计算余弦相似度
        cosine_similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        # 获取最相似的文档的索引
        related_docs_indices = cosine_similarities.argsort()[:-top_n-1:-1]
        return [(self.blocks[index], cosine_similarities[index]) for index in related_docs_indices]

    def get_answer(self, query, answer_index=None):
        # 需要查询前三个索引找出最近的章节,有可能有相似的题目干扰，需要遍历查找
        answer_similar_list = self.find_similar(query)
        query_text = remove_punctuation(query)
        answer_block = ""
        # 非文本向量化即采用idf-tf算法需要这么做
        for index,answer_obj in enumerate(answer_similar_list):
            similar_block = answer_obj[0]
            # 对问题和答案进行去标点，防止匹配的时候有空格和标点影响，只匹配文字
            clean_text = remove_punctuation(similar_block)
            # print(query_text)
            if query_text in clean_text:
                answer_block = similar_block
                print(f"找到答案,{answer_block}")
                break
        if answer_block == "":
            print("未找到答案，已使用tf-idf算法为你寻找最相似答案")
            answer_block = answer_similar_list[0][0]
        if answer_index is not None:
            answer_block = answer_similar_list[answer_index][0]
            print(f"已重新规划,为您寻找第{answer_index}相似的答案,{answer_block}")
        # 将answer按照换行切分
        answer_list = answer_block.split('\n')
        # 答案文本
        answer_text = ""
        # 题目中选项
        option_text_list = ""
        for index, line in enumerate(answer_list):
            if '答案' in line:
                # answer_text为从这个索引开始到结束
                answer_text = ''.join(answer_list[index:])
                option_text_list = answer_list[:index]
        # 根据标点分词答案
        answer_text = split_by_punctuation(answer_text, option_text_list)

        return answer_text

class Ocr:
    def __init__(self):
        self.model = self.init_ocr()

    def init_ocr(self):
        # 当前脚本位置
        base_path = os.getcwd()
        relative_path = 'Ocr_Model'
        custom_model_path = os.path.join(base_path, relative_path)
        os.environ['CNOCR_HOME'] = custom_model_path
        ocr = CnOcr(
            det_model_name='naive_det',
            rec_root='/Model/Ocr_Model/cnocr',  # 自定义识别模型存储目录
            det_root='/Model/Ocr_Model/cnstd'  # 自定义检测模型存储目录
        )
        return ocr

    def ocr_img(self, img_data):
        # 若为二进制数据
        out = ""
        if isinstance(img_data, bytes):
            image = Image.open(BytesIO(img_data))
            out = self.model.ocr(image)
        # 若为本地路径，则使用以下代码
        elif os.path.exists(img_data):
            out = self.model.ocr(img_data)
        # 若为网络图片
        elif re.match(r'^https?:\/\/', img_data):
            response = requests.get(img_data)
            image = Image.open(BytesIO(response.content))
            out = self.model.ocr(image)
        out_text = out[0]['text']

        return out_text

if __name__ == '__main__':
    from Util.AnswerCrawl_Util import AnswerCrawl
    answer_obj = AnswerCrawl('创造性思维与创新方法（大连理工大学）')
    answer_blocks = answer_obj.getAnswerText_Mode0()
    from time import time
    strat_time = time()
    ocr = Ocr()
    end_time = time()
    print(f"ocr初始化耗时{end_time-strat_time}")
    answerQuery = AnswerQuery(answer_blocks)
    end_answer_time = time()
    print(f"answerQuery初始化耗时{end_answer_time-end_time}")
    answer = answerQuery.get_answer('依照赫曼全脑模型划分，孙悟空属于（ ）')
    print(f"answerQuery耗时{time()-end_answer_time}")
    print(answer)