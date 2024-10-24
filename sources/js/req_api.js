const req_api = {
    login: function(account,password,update) {
        // 调用 Python 中的 login 方法
        return pywebview.api.login(account,password,update).then(response => {
            return response;  // 返回响应以便可以处理响应数据
        }).catch(error => {
            alert('Error logging in:',error.message);
            throw error;  // 抛出错误以便可以捕获并处理
        });
    },
    openpage: function(question,url) {
        // 调用 Python 中的 login 方法
        return pywebview.api.open_page(question,url).then(response => {
            return response;  // 返回响应以便可以处理响应数据
        }).catch(error => {
            alert('Error logging in:',error.message);
            throw error;  // 抛出错误以便可以捕获并处理
        });
    },
    do_test:function(courese_name,classindex, answer_url) {
        // 调用 Python 中的 login 方法
        return pywebview.api.do_test(courese_name,classindex,answer_url).then(response => {
            return response;  // 返回响应以便可以处理响应数据
        }).catch(error => {
            alert('Error logging in:',error.message);
            throw error;  // 抛出错误以便可以捕获并处理
        });
    },
    watchVideo:function(classindex) {
        // 调用 Python 中的 login 方法
        return pywebview.api.watch_video(classindex).then(response => {
            return response;  // 返回响应以便可以处理响应数据
        }).catch(error => {
            alert('Error logging in:',error.message);
            throw error;  // 抛出错误以便可以捕获并处理
        });
    },
    getClassInfoList:function(userInfo,userIndex) {
        // 调用 Python 中的 login 方法
        return pywebview.api.get_classinfo_list(userInfo,userIndex).then(response => {
            return response;  // 返回响应以便可以处理响应数据
        }).catch(error => {
            alert('Error logging in:',error.message);
            throw error;  // 抛出错误以便可以捕获并处理
        });
    },
    getLogContent: function () {
        // 读取本地日志文件内容
        return pywebview.api.get_log_content().then(response => {
            return response;  // 返回响应以便可以处理响应数据
        }).catch(error => {
            alert('Error logging in:',error.message);
            throw error;  // 抛出错误以便可以捕获并处理
        });
    },
    CheckUpdate: function () {
        // 读取本地日志文件内容
        return pywebview.api.check_update().then(response => {
            return response;  // 返回响应以便可以处理响应数据
        }).catch(error => {
            alert('Error logging in:',error.message);
            throw error;  // 抛出错误以便可以捕获并处理
        });
    },


};

export default req_api;
