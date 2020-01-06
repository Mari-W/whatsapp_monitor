#!/usr/bin/python3

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import strftime, sleep
from collections import defaultdict
import traceback
import os
import psutil

for proc in psutil.process_iter():
    if proc.name() == "display":
        proc.kill()
# Set up selenium
print("Setting up..")
# you may also want to remove whitespace characters like `\n` at the end of each line
with open("config.cfg") as f:
    content = f.readlines()
    f.close()

lines = [x.strip() if "#" not in x else "" for x in content]
content = list(filter(lambda item: item.strip(), lines))

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36")
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=options)

names = content

# Redirect to whatsapp and read qr code
print("Redirecting to Whatsapp..")
driver.get("http://web.whatsapp.com")
sleep(1)

# save qr code as screenshot
with open('qr_waw.png', 'wb') as file:
    file.write(
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div/img').screenshot_as_png)
print("Scan generated QR code to continue..")

while True:
    try:
        chat = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[2]/div")

        for proc in psutil.process_iter():
            if proc.name() == "display":
                proc.kill()

        chat.click()
        sleep(2)
        search = driver.find_element_by_xpath(
            "//*[@id=\"app\"]/div/div/div[2]/div[1]/span/div/span/div/div[1]/div/label/input")
        search.click()
        search.send_keys(names[0])
        search.send_keys(Keys.ENTER)

        sleep(1)

        print("Able to interact with WhatsApp!")
        i = 0

        last = defaultdict(lambda: (0, ''))

        os.remove("qr_waw.png")

        while True:
            t = strftime("%Y-%m-%d %H:%M:%S")
            name = names[i]

            if not os.path.exists(name + ".csv"):
                log = open(name + ".csv", "a+")
                log.write("From,To\n")
            else:
                log = open(name + ".csv", "a+")

            # noinspection PyBroadException
            try:
                search = driver.find_element_by_xpath(
                    "//*[@id=\"side\"]/div[1]/div/label/input")
                search.click()
                search.clear()
                search.send_keys(name)
                sleep(1)
                search.send_keys(Keys.ENTER)
                status = driver.find_element_by_class_name("_315-i").text
                state = 1 if 'online' in status else 0
                time = "{0}".format(strftime("%d/%m/%Y-%H:%M:%S"))
                last_state, last_time = last[name]
                if state != last_state:
                    if state == 0:
                        log.write("{0},{1}\n".format(last_time, time))
                    last[name] = state, time
            except Exception:
                time = "{0}".format(strftime("%d/%m/%Y-%H:%M:%S"))
                last_state, last_time = last[name]
                if 0 != last_state:
                    log.write("{0},{1}\n".format(last_time, time))
                    last[name] = 0, time
                pass

            if i == len(names) - 1:
                with open("config.cfg") as f:
                    content = f.readlines()
                    f.close()
                names = [x.strip() for x in content][(content.index("#contacts\n") + 1):]
                i = 0
            else:
                i += 1

            log.close()

    except Exception as e:
        print(":Please Scan QR code or an error appeared:")
        sleep(2)
        traceback.print_exc()
        print(str(e))
