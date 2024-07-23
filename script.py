import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time

def get_weather():
    url = "https://www.bbc.com/weather/2158177"  # 墨尔本的BBC Weather页面
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to retrieve the weather information. Status code: {response.status_code}"

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        temperature_max_element = soup.find('span', class_='wr-day-temperature__high-value')
        temperature_min_element = soup.find('span', class_='wr-day-temperature__low-value')
        condition_element = soup.find('div', class_='wr-day__weather-type-description')
        wind_element = soup.find('span', class_='wr-value--windspeed--mph')
        sunrise_element = soup.find('span', {'data-testid': 'sunrise'})
        sunset_element = soup.find('span', {'data-testid': 'sunset'})

        # Check if elements exist and extract text
        temperature_max = temperature_max_element.text.strip() if temperature_max_element else "N/A"
        temperature_min = temperature_min_element.text.strip() if temperature_min_element else "N/A"
        condition = condition_element.text.strip() if condition_element else "N/A"
        wind = wind_element.text.strip() if wind_element else "N/A"
        sunrise = sunrise_element.text.strip() if sunrise_element else "N/A"
        sunset = sunset_element.text.strip() if sunset_element else "N/A"

        weather_info = (
            f"Max Temperature: {temperature_max}\n"
            f"Min Temperature: {temperature_min}\n"
            f"Condition: {condition}\n"
            f"Wind Speed: {wind}\n"
            f"Sunrise: {sunrise}\n"
            f"Sunset: {sunset}\n"
        )

        greeting = "Good morning XiXi! I love you so much!!! Wish you have a perfect day!"
        return weather_info + "\n" + greeting

    except AttributeError as e:
        return f"Failed to parse the weather information: {e}"

def send_email(subject, body, to_email):
    from_email = "212337984@qq.com"
    from_password = "mrtbcwbfeyeibgeb"

    server = smtplib.SMTP('smtp.qq.com', 587)
    server.starttls()
    try:
        server.login(from_email, from_password)
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
        return
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {e}")
        return

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server.send_message(msg)
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

def job():
    subject = "Today's Weather in Melbourne"
    body = get_weather()
    to_email = "350738767@qq.com"
    send_email(subject, body, to_email)

# 安排每日发送
schedule.every().day.at("08:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)