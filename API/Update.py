import requests
import json
def _check_update():
    url = 'https://raw.githubusercontent.com/666cy666/Script-Zhihuishu/refs/heads/main/sources/Settings/Config_Setting.json'
    version_text = requests.get(url).text
    version_json = json.loads(version_text)
    version = version_json["check_update"]["version"]
    return version



