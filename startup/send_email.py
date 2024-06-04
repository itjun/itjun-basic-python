import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_email(subject, body):
    # 电子邮件服务器配置
    smtp_server = 'smtp.qq.com'
    smtp_port = 465
    sender_email = 'l1091462907@qq.com'
    sender_password = 'dxsxgouvuerchegb'
    recipient_email = '13927470636@139.com'  # 接收邮件地址

    # 创建邮件内容
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # 连接到邮件服务器并发送邮件
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print('Email sent successfully')
            server.quit()
    except Exception as e:
        print(f'Failed to send email: {e}')

# 获取当前日期和时间
now = datetime.now()
# 格式化日期和时间
current_date_and_time = now.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'startup':
        send_email('itjun-alpha 启动', f'{current_date_and_time} Your computer has just started.')
    elif len(sys.argv) > 1 and sys.argv[1] == 'shutdown':
        send_email('itjun-alpha 关机', f'{current_date_and_time} Your computer is shutting down.')
