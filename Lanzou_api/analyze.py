import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6'
}

# 取中间字符串
def extract_text(input_text, left_condition, right_condition):
    # 构建正则表达式
    pattern = re.compile(
        f'{re.escape(left_condition)}(.*?){re.escape(right_condition)}')

    # 使用正则表达式查找匹配项
    match = re.findall(pattern, input_text)
    return match

### 给定3个参数-分享的文件夹链接 带密码
def param3(url_param, psw_param, fname_param):
    result = ''
    ###### 1 根据分享链接及密码并获取参数
    try:
        main_url = extract_text(url_param, '://', '.com')[0]
        response = requests.get(url_param, headers=headers)
        if response.status_code != 200:
            return f"{url_param} 请求失败faild-400，状态码：{response.status_code}"
        else:
            pg1 = extract_text(response.text, "'pg':", ",")[0]
            t1 = extract_text(response.text, "'t':", ",")[0]
            k1 = extract_text(response.text, "'k':", ",")[0]
            data = {
                'lx': extract_text(response.text, "'lx':", ",")[0],
                'fid': extract_text(response.text, "'fid':", ",")[0],
                'uid': extract_text(response.text, "'uid':'", "'")[0],
                'pg': extract_text(response.text, f"{pg1} =", ";")[0],
                'rep': extract_text(response.text, "'rep':'", "'")[0],
                't': extract_text(response.text, f"var {t1} = '", "'")[0],
                'k': extract_text(response.text, f"var {k1} = '", "'")[0],
                'up': extract_text(response.text, "'up':", ",")[0],
                'ls': extract_text(response.text, "'ls':", ",")[0],
                'pwd': psw_param
            }
    except:
        return f"{url_param} 请求失败faild-400"
    ###### 2 根据密码发送post请求
    try:
        response = requests.post("https://" + main_url + ".com/filemoreajax.php", headers=headers, data=data)
        if response.status_code != 200:
            return f"https://{main_url}.com/filemoreajax.php 请求失败faild-400，状态码：{response.status_code}"
        data = response.json()
        if data['info'] != 'sucess':
            return f"https://{main_url}.com/filemoreajax.php 请求失败faild-400，状态码：{response.status_code}"
    except:
        return f"https://{main_url}.com/filemoreajax.php 请求失败faild-400"
    ###### 3 解析返回的json
    try:
        for ii in data['text']:
            if ii['name_all'] == fname_param:
    ###### 4 解析出文件id, 并获取fn
                try:
                    response = requests.get("https://" + main_url + ".com/"+ii['id'], headers=headers)
                    if response.status_code != 200:
                        return f"https://{main_url}.com/{ii['id']} 请求失败faild-400，状态码：{response.status_code}"
                    else:
                        fn = extract_text(response.text, 'src="', '" frameborder')[1]
                except:
                    return f"https://{main_url}.com/{ii['id']} 请求失败faild-400"
    ###### 5 解析fn
                try:
                    response = requests.get("https://" + main_url + ".com/"+fn, headers=headers)
                    if response.status_code != 200:
                        return f"https://{main_url}.com/{fn} 请求失败faild-400，状态码：{response.status_code}"
                    else:
                        signs1 = extract_text(response.text, "'signs':", ",")[0]
                        websignkey1 = extract_text(response.text, "'websignkey':", ",")[0]
                        data = {
                            'action': extract_text(response.text, "'action':'", "'")[0],
                            'signs': extract_text(response.text, f"{signs1} = '", "'")[0],
                            'sign': extract_text(response.text, "'sign':'", "'")[0],
                            'websign': "",
                            'websignkey': extract_text(response.text, f"{websignkey1} = '", "'")[0],
                            'ves': extract_text(response.text, "'ves':", " ")[0]
                        }
                except:
                    return f"https://{main_url}.com/{fn} 请求失败faild-400"
    ###### 6 获取伪直链
                try:
                    headers2 = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
                        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
                        'Referer': "https://" + main_url + ".com/"+fn
                    }
                    response = requests.post("https://"+main_url+".com/ajaxm.php", headers=headers2, data=data)
                    if response.status_code != 200:
                        return f"https://{main_url}.com/ajaxm.php 请求失败faild-400，状态码：{response.status_code}"
                    else:
                        data = response.json()
                        fake_downurl = data['dom'] + '/file/' + data['url']
                except:
                    return f"https://{main_url}.com/ajaxm.php 请求失败faild-400"
    ###### 7 获取真直链
                try:
                    response = requests.get(fake_downurl, headers=headers, allow_redirects=False)
                    if response.status_code != 302:
                        return f"{fake_downurl} 伪直链请求失败faild-400，状态码：{response.status_code}"
                    else:
                        for key, value in response.headers.items():
                            if key == 'Location':
                                result = value
                                return value
                                # true_downurl = value
                except:
                    return f"{fake_downurl} 伪直链请求失败faild-400"
        if result == '':
            return "请求失败faild-400"
    except:
        pass

### 给定2个参数-分享的是文件链接 带密码
def param2(url_param, psw_param):
    pass

### 给定1个参数-分享的是文件 不带密码
def param1(url_param):
    result = ''
    ###### 1 根据文件id, 并获取fn
    try:
        main_url = extract_text(url_param, '://', '.com')[0]
        response = requests.get(url_param, headers=headers)
        if response.status_code != 200:
            return f"{url_param} 请求失败faild-400，状态码：{response.status_code}"
        else:
            fn = extract_text(
                response.text, 'src="', '" frameborder')[0]
    except:
        return f"{url_param} 请求失败faild-400"
###### 2 解析fn
    try:
        response = requests.get(
            "https://" + main_url + ".com/"+fn, headers=headers)
        if response.status_code != 200:
            return f"https://{main_url}.com/{fn} 请求失败faild-400，状态码：{response.status_code}"
        else:
            signs1 = extract_text(
                response.text, "'signs':", ",")[0]
            websignkey1 = extract_text(
                response.text, "'websignkey':", ",")[0]
            data = {
                'action': extract_text(response.text, "'action':'", "'")[0],
                'signs': extract_text(response.text, f"{signs1} = '", "'")[0],
                'sign': extract_text(response.text, "'sign':'", "'")[0],
                'websign': "",
                'websignkey': extract_text(response.text, f"{websignkey1} = '", "'")[0],
                'ves': extract_text(response.text, "'ves':", " ")[0]
            }
    except:
        return f"https://{main_url}.com/{fn} 请求失败faild-400"
###### 3 获取伪直链
    try:
        headers2 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
            'Referer': "https://" + main_url + ".com/"+fn
        }
        response = requests.post(
            "https://"+main_url+".com/ajaxm.php", headers=headers2, data=data)
        if response.status_code != 200:
            return f"https://{main_url}.com/ajaxm.php 请求失败faild-400，状态码：{response.status_code}"
        else:
            data = response.json()
            fake_downurl = data['dom'] + '/file/' + data['url']
    except:
        return f"https://{main_url}.com/ajaxm.php 请求失败faild-400"
###### 4 获取真直链
    try:
        response = requests.get(
            fake_downurl, headers=headers, allow_redirects=False)
        if response.status_code != 302:
            return f"{fake_downurl} 伪直链请求失败faild-400，状态码：{response.status_code}"
        else:
            for key, value in response.headers.items():
                if key == 'Location':
                    result = value
                    return value
                    # true_downurl = value
    except:
        return f"{fake_downurl} 伪直链请求失败faild-400"
    if result == '':
        return "请求失败faild-400"
