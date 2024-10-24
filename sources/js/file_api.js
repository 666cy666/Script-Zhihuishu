const paths = {
    config_Info: 'sources//Settings//Config_Setting.json',
    user_Info: 'sources//Settings//User_Setting.json',
    memory_Info: 'sources//Settings//Memory_Setting.json',
    about_Info: 'sources//Settings//About_Setting.json',

    log_info: 'Log//log.txt'
    // 其他路径...
};

const file_api = {
    getJsonData: function (filePath) {
        return fetch(filePath)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                return data;
            })
            .catch(error => {
                alert('Failed to get data:', error);
                throw error;
            });
    },
    

    getConfigInfo: function () {
        return this.getJsonData(paths.config_Info);
    },
    getUserInfoList: function () {
        // console.log(this.getJsonData(paths.userInfo));
        return this.getJsonData(paths.user_Info);
    },
    getMemoryInfo: function () {
        // console.log(this.getJsonData(paths.userInfo));
        return this.getJsonData(paths.memory_Info);
    },
    getAboutSetting: function () {
        // console.log(this.getJsonData(paths.userInfo));
        return this.getJsonData(paths.about_Info);
    },
    // addUserInfo:function() {
    //     return this.getJsonData(paths.userInfo);
    // },   
    updateConfigInfo: function (newConfig) {
        return pywebview.api.update_config_info(newConfig)
            .then(response => {
                // alert('Config updated successfully:', response);
            })
            .catch(error => {
                alert('Failed to update config:', error);
            });
    },
    updateMemoryInfo: function (newMemory) {
        return pywebview.api.update_memory_info(newMemory)
            .then(response => {
                // alert('Config updated successfully:', response);
            })
            .catch(error => {
                alert('Failed to update config:', error);
            });
    },
    update_UserinfoList: function (userInfoList) {
        return pywebview.api.update_userinfo(userInfoList).then(response => {
            return response;  // 返回响应以便可以处理响应数据
        }).catch(error => {
            alert('Error logging in:', error.message);
            throw error;  // 抛出错误以便可以捕获并处理
        });
    },
    update_Userinfo_By_Index: function (userInfo, userIndex) {
        return pywebview.api.update_userinfo_by_index(userInfo, userIndex).then(response => {
            return response;  // 返回响应以便可以处理响应数据
        }).catch(error => {
            alert('Error logging in:', error.message);
            throw error;  // 抛出错误以便可以捕获并处理
        });
    }

};


export default file_api;
