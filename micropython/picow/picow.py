import network
import time
from machine import Pin
import ubinascii
import requests

# 默认ssid与密码
def_wifi_ssid = "knowall"
def_wifi_password = "Ka2004"
machine_num = 2  # 配置了2个ds18b20，最大值为9
# origin = "picow" + machine_num # 固定在代码中
origin = "picow" # 固定在代码中

# 板载LED引脚初始化（Pico W 的板载 LED 引脚是 0）
LED_PIN = 'LED'
led = Pin(LED_PIN, Pin.OUT)

# 读取CPU温度
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

# 读取本地配置
config_file = "config.txt"
try:
    with open(config_file, 'r') as f:
        lines = f.readlines()
except FileNotFoundError:
    print("config.txt not found")
    led.value(1)  # 故障亮灯
    exit()
for line in lines:
    print(line)

def read_properties(lines, key, defValue):
    for line in lines:
        arr = line.strip().split("=")
        if len(arr) > 0:
            key1 = arr[0]
            value = arr[1]
            if key1.strip()==key:
                return value.strip()
    return defValue

# 配置版本号，默认值1
version = read_properties(lines, "version", "0")

# 网络配置
wifi_ssid = read_properties(lines, "wifi_ssid", "abcdefg")
print(wifi_ssid)
wifi_password = read_properties(lines, "wifi_password", "123456")
print(wifi_password)

# 硬件讯息
token = read_properties(lines, "token", "")
machine = read_properties(lines, "machine", "")
precision = read_properties(lines, "precision", "") # 单位：摄氏度，默认值0.5
frequency = read_properties(lines, "frequency", "") # 单位：秒，默认值10

def read_pico_temperature():
    # 读取原始ADC值
    reading = sensor_temp.read_u16()
    # 转换为电压
    voltage = reading * conversion_factor
    # 根据树莓派 Pico 的数据手册，转换电压为温度
    temperature = 27 - (voltage - 0.706) / 0.001721
    return temperature

def read_ds18b20(index):
    return 20

def led_flashing(timer, count):
    for _ in range(0, count):
        led.value(1)  # 打开LED
        time.sleep(timer)
        led.value(0)  # 关闭LED
        time.sleep(timer)

# 初始化WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def connection(ssid, password):
    # 连接到WiFi网络
    wlan.connect(ssid, password)

    # 等待连接
    max_wait = 10
    while max_wait > 0:
        if wlan.isconnected():
            break
        print(f"正在连接到 WiFi... SSID: {ssid}, Password: {password}")
        led.value(1)  # 打开LED
        time.sleep(0.5)
        led.value(0)  # 关闭LED
        time.sleep(0.5)
        max_wait -= 1

    # 检查连接状态
    if wlan.isconnected():
        print('连接成功')
        print('网络配置:', wlan.ifconfig())

        # 获取并显示 MAC 地址
        mac = ubinascii.hexlify(wlan.config('mac'), ':').decode()
        print('MAC 地址:', mac)
        return True
    else:
        print('无法连接到 WiFi')
        return False

print(f"正在连接到 WiFi... SSID: {wifi_ssid}, Password: {wifi_password}, version: {version}")

# 连接 WiFi
count = 0
while count < 100:
    print(f"setp01 {count}")
    if count == 3 and version > 0:
        print(f"setp01-1 {count}")
        wifi_ssid = def_wifi_ssid
        wifi_password = def_wifi_password
    
    print(f"setp01-2 {count}")
    wifi = connection(wifi_ssid, wifi_password)
    print(f"wifi {wifi}")

    if not wifi:
        print(f"setp02 {count}")
        time.sleep(100)
        led_flashing(0.5, 10)
        count = count + 1
        time.sleep(1000) #1秒后再试
    else:
        print(f"setp03 {count}")
        break

print(f"setp04 {count}")


# 连接到云端
# upload_flag = 0
data = range(0, machine_num) # 9999
for line in data:
    line = 9999
while True:
    # 读取温度数据
    cpu_temp = read_pico_temperature() # 读取pico 内置的温度
    # 读取 ds18b20 温度
    # for i in range(0, machine_num):
    #     temp = read_ds18b20(i)
    #     if data[i] == 9999 or abs(temp, data[i]) > precision:
    #         upload_flag = 999999 # 大于24 * 3600秒即可
    #         data[i] = temp

    # if upload_flag == 0:
        # 每一次循环均加上一个值，这个值需要根据实际耗时来调整
        # upload_flag = upload_flag + 1

    # 判断是否需要上传
    # if upload_flag < frequency:
        # time.sleep(100)
        # continue

    # 提交到网站
    # upload_flag = 0 # 重置此参数
    data = {
        "machine": machine,
        "origin": origin,
        "message": "温度上传",
        'level': 'debug',
        'type': 'pico',
        'machine': 'pico_w_local_mac_ip',
        "data0": cpu_temp
    }
    # TODO 构建动态字典
    # for i in range(0, machine_num):
    #    data[data.__len__] =  "data" + i,  "温度感应器",

    url = ['https://qc.4plc.cn/public/log1?token={}&version={}', token, version]
    # 请求头
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
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
            json = response.json()  # 解析 JSON 响应
            state = json.get('state')
            message = json.get('message')
            if state < 1:   # 错误时快闪灯3秒
                print('调用失败，后台返回: {}', message)
                led_flashing(250, 12)
            else:
                if state == 1:
                    print('调用成功，后台返回：{}', message)
                else:
                    if json.startWith('version='):
                        #write message to file config_file
                        print("writer to file")
                        #soft reset //重启pcio
                    else: # 错误时慢闪灯10秒
                        print('返回数据格式错误: {}', message)
                        led_flashing(500, 20)
            time.sleep(100)
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print("响应内容:")
            print(response.text)

    except requests.RequestException as e:
        print(f"请求出现异常: {e}")


