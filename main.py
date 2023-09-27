from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import os
import traceback
import requests
import os
import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
MY_ADDRESS = 'serveralert@webdev.asia'
PASSWORD = 'bDIZ014O?&pc'


current_dir = "/var/www/flaskapp/flaskapp"
def driver_start():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no visible browser window)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (may help with headless mode stability)
    chrome_options.add_argument("--no-sandbox")  # Disable sandboxing (useful for some environments)
    chrome_options.add_argument("--start-maximized")

    chrome_options.add_argument("--remote-debugging-port=9222")  # this
    chrome_options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")

    chrome_options.add_argument("--disable-dev-shm-using") 
    chrome_options.add_argument("--disable-extensions") 
    current_dir = "/var/www/flaskapp/flaskapp"  # Get the current directory


    chrome_options.add_argument(f'--user-data-dir={current_dir}/new_profile')  # Set user data directory in current directory
# Set user data directory in current directory
    chromedriver_path = "/usr/bin/chromedriver"
    from selenium.webdriver.chrome.service import Service
    service = Service(executable_path=chromedriver_path)

# Initialize the Chrome browser
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver



app = Flask(__name__)

def download_media_file(image_url):

    # Directory where you want to save the image
    save_directory = "/var/www/flaskapp/flaskapp/uploads"

    # Create the directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Get the filename from the URL
    filename = os.path.join(save_directory, os.path.basename(image_url))

    # Send an HTTP GET request to the image URL
    response = requests.get(image_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Open a local file with the same name as the original image
        with open(filename, "wb") as file:
            # Write the content of the response to the local file
            file.write(response.content)
        print(f"Image downloaded and saved as {filename}")
        return filename
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        return None



def creat_n_send_msg(data):
    try:    
          
        driver=driver_start()
        print("driver started")
        wait = WebDriverWait(driver, 120)

        # open whatsapp grp
        driver.get("https://web.whatsapp.com/accept?code=JXg5P4ZdOziHbyzcTcWen8")
        driver.save_screenshot(f"{current_dir}/2.png")
        wp_input_btn = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div[1]/div[1]/p')))
        driver.save_screenshot(f"{current_dir}/error2.png")
        wp_input_btn.click()
        time.sleep(2)
        msg_txt = f"Rider's Name: {data.get('riders_name')}\n Rider's HP Number: {data.get('riders_hp_number')}\n Email Address: {data.get('email_address')}\n Bike Number: {data.get('bike_number')}\n Bike Model: {data.get('bike_model')}\n Location Pickup: {data.get('location_pickup')}\n Location Type: {data.get('location_type')}\n Carpark Level: {data.get('carpark_level')}\n Carpark Max Height: {data.get('carpark_max_height')}\n Location Deliver: {data.get('location_deliver')}\n Reason Towing: {data.get('reason_towing')}\n Handle Unlocked: {data.get('handle_unlocked')}\n Other Details: {data.get('other_details')}\nAttachment Url: https://jeyaprakash.com/form2/{data.get('media_path')}"
        br = (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT)
        text = f"Rider's Name: {data.get('riders_name')}"+br+f"Rider's HP Number: {data.get('riders_hp_number')}"+br+f"Email Address: {data.get('email_address')}"+br+f"Bike Number: {data.get('bike_number')}"+br+f"Bike Model: {data.get('bike_model')}"+br+f"Location Pickup: {data.get('location_pickup')}"+br+f"Location Type: {data.get('location_type')}"+br+f"Carpark Level: {data.get('carpark_level')}"+br+f"Carpark Max Height: {data.get('carpark_max_height')}"+br+f"Location Deliver: {data.get('location_deliver')}"+br+f"Reason Towing: {data.get('reason_towing')}"+br+f"Handle Unlocked: {data.get('handle_unlocked')}"+br+f"Other Details: {data.get('other_details')}"
        send_email("RESPONSE",msg_txt) 
        wp_input_btn.send_keys(text)
        time.sleep(1)
        driver.save_screenshot(f"{current_dir}/input.png")

        element = wait.until(EC.element_to_be_clickable((By.XPATH , '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span'))).click()
        driver.save_screenshot(f"{current_dir}/input2.png")
        time.sleep(2)

        # wait for msg to be send and deliver
        driver.save_screenshot(f"{current_dir}/input3.png")
        time.sleep(10)
        driver.save_screenshot(f"{current_dir}/input4.png")

        print("msg sent without media")
        if data.get("media_path"):
            print("found media")
            try:
                file_path = download_media_file(f'https://jeyaprakash.com/form2/{data.get("media_path")}')
                print(file_path)
                print("downloaded media")
            except Exception as e:
                print(e)
                file_path = None
            if file_path:
                driver.save_screenshot(f"{current_dir}/attachment.png")
                attachment_icon = driver.find_element(By.XPATH,'//div[@title="Attach"]')
                attachment_icon.click()
                time.sleep(2)
                driver.save_screenshot(f"{current_dir}/attachment2.png")

                element = driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div/div/span/div/ul/div/div[1]/li/div/input')    
                driver.save_screenshot(f"{current_dir}/attachment3.png")   
                time.sleep(15)
                driver.save_screenshot(f"{current_dir}/attachment4.png")

                element.send_keys(file_path)
                driver.save_screenshot(f"{current_dir}/attachment5.png")
                time.sleep(1)
                driver.save_screenshot(f"{current_dir}/error.png")
                driver.save_screenshot(f"{current_dir}/attachment6.png")
                element = driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/div[1]/p')
                time.sleep(2)
                driver.save_screenshot(f"{current_dir}/attachment7.png")
                element.click()
                driver.save_screenshot(f"{current_dir}/attachment8.png")
                time.sleep(1)
                driver.save_screenshot(f"{current_dir}/error.png")
                driver.save_screenshot(f"{current_dir}/attachment9.png")

                element.send_keys(Keys.ENTER)
                driver.save_screenshot(f"{current_dir}/error.png")
                driver.save_screenshot(f"{current_dir}/attachment10.png")



    # Wait for the message to send
        time.sleep(5)

               # qr = generate_qr()
        print("sent msg")
    except Exception as e:
        send_email("ERROR",{str(e)})
        print(f"Error: {str(e)} {traceback.print_exc()}", 500)




@app.route('/sendmsg', methods=['POST'])
def send_webhook():
    try:
        data = request.get_json()
        print(data)
        thread = threading.Thread(target=creat_n_send_msg, args=(data,))
        thread.start()        
        print("done done")
        return data
    except Exception as e:
        print(f"Error: {str(e)} {traceback.print_exc()}", 500)
        send_email("ERROR",str(e))
        return "error"


@app.route('/check_current', methods=['POST'])
def check_current():
    try:
        driver=driver_start()
        driver.get("https://web.whatsapp.com/")
        driver.save_screenshot(f"{current_dir}/error.png")
        wait = WebDriverWait(driver, 120)
        time.sleep(100)
        driver.save_screenshot(f"{current_dir}/error4.png")
 
        # Adjust the timeout as needed
        element = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]')))
        element
        #with open(f"{current_dir}/index3.html" , "w" ,encoding="utf8") as f:
             #f.write(str(driver.page_source))
        driver.save_screenshot(f"{current_dir}/error2.png")
        return "dont"
    except Exception as e:
        send_email("ERROR",e)

        return f"Error: {str(e)} {traceback.print_exc()}", 500

def send_email(subject,message):
    try:
        message = str(message)
        s = smtplib.SMTP(host='mail.webdev.asia', port=587)
        s.starttls()
        s.login(MY_ADDRESS, PASSWORD)
        msg = MIMEMultipart()
        msg['From']=MY_ADDRESS
        msg['To']='arijitghosal0309@gmail.com'
        msg['Subject']=subject
                
        msg.attach(MIMEText(message, 'plain'))
        s.send_message(msg)
    except Exception as e:
        print(e)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

