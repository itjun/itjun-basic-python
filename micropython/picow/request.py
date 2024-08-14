import requests

# from urllib.parse import urlencode

url = 'https://qc.4plc.cn/public/log1?token=1806118688ac4c2ba9456ab21c93013c'

# 请求头
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

# 请求数据
data = {
    'origin': 'pico_w',
    'message': '温度上传',
    'level': 'value2',
    'type': 'value2',
    'machine': 'pico_w_local_mac_ip',
    'createTime': '1716896462112',  # 2024-05-24 18:05:35
    'data0': '21',
    'data1': '22',
}

try:
    # 使用 urlencode 对数据进行 UTF-8 编码
    # encoded_data = urlencode(data, encoding='utf-8')

    # 发起 POST 请求
    response = requests.post(url, headers=headers, data=data)

    # 检查响应状态码
    if response.status_code == 200:
        print("请求成功:")
        print(response.text)
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print("响应内容:")
        print(response.text)

except requests.RequestException as e:
    print(f"请求出现异常: {e}")
