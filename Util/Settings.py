import sys
sys.path.append('./Util')
import os

from Util.File_Util import get_json_info

user_info_path = os.path.join("sources", "Settings", "User_Setting.json")
config_info_path = os.path.join("sources", "Settings", "Config_Setting.json")
memory_info_path = os.path.join("sources", "Settings", "Memory_Setting.json")

user_info_list = get_json_info(user_info_path)

if __name__ == "__main__":
    print(user_info_path)

