import network
import time
from machine import Pin
import ubinascii

# WiFi 配置
SSID = 'MIMRC-RDC6'  # 将 'your-SSID' 替换为你的 WiFi 网络名称
PASSWORD = 'Mi12345678'  # 将 'your-password' 替换为你的 WiFi 密码

# 初始化WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# 板载LED引脚初始化（Pico W 的板载 LED 引脚是 0）
LED_PIN = 'LED'
led = Pin(LED_PIN, Pin.OUT)

# 连接到WiFi网络
wlan.connect(SSID, PASSWORD)

# 读取CPU温度
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)


def read_temp():
    # 读取原始ADC值
    reading = sensor_temp.read_u16()
    # 转换为电压
    voltage = reading * conversion_factor
    # 根据树莓派 Pico 的数据手册，转换电压为温度
    temperature = 27 - (voltage - 0.706) / 0.001721
    return temperature


temp = read_temp()
print('当前CPU温度:', temp, '°C')

# 等待连接
max_wait = 10
while max_wait > 0:
    if wlan.isconnected():
        break
    print('正在连接到 WiFi...')
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

    # WiFi连接成功后，让LED闪烁
    for _ in range(100):  # 闪烁10次
        led.value(1)  # 打开LED
        time.sleep(0.5)
        led.value(0)  # 关闭LED
        time.sleep(0.5)
else:
    print('无法连接到 WiFi')

    # WiFi连接失败后，让LED快速闪烁
    for _ in range(5):  # 快速闪烁20次
        led.value(1)  # 打开LED
        time.sleep(0.1)
        led.value(0)  # 关闭LED
        time.sleep(0.1)

# 保持程序运行，不让它立即结束
try:
    while True:
        pass
except KeyboardInterrupt:
    # 捕捉键盘中断信号，确保在终端中按Ctrl+C时能优雅地退出
    led.value(0)  # 程序结束时关闭LED
    print("程序被中断，LED已关闭")
