log_path = './Log/log.txt'


class StdoutRedirector:
    def __init__(self, log_file):
        self.log_file = log_file
        self.clear_log_file()

    def clear_log_file(self):
        with open(self.log_file, 'w', encoding='gbk') as f:
            f.write('')  # 清空日志文件内容

    @staticmethod
    def read_log_file():
        with open(log_path, 'r', encoding='utf-8') as f:
            log_content = f.read()
            return log_content

    def write(self, message):
        if message.strip():
            with open(self.log_file, 'r+', encoding='utf-8') as f:
                existing_content = f.read()
                f.seek(0)
                f.write('\n'+ message + '\n' + existing_content)

    def flush(self):
        pass


