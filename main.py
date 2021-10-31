from __future__ import division, print_function, absolute_import, unicode_literals
import os
import io
import sys
import time
import enum
import argparse
import datetime
from fpdf import FPDF 
from PIL import Image
from selenium import webdriver
from colorama import init, Fore 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support import expected_conditions as EC 

# General Paremters
PATH = os.getcwd()

# Set your credentials here
USERNAME = ''
PASSWORD = ''
H,W = 1300, 884

# Cropping Tuples
A4_CROP = (338, 0, 912, 796)
SQ_CROP = (228, 0, 1028, 795) # Square Crop

# Task: Add colored text in termianl (Colorama lib) 
init(autoreset=True, convert=True)

def parseArguments():
    parser = argparse.ArgumentParser(description='Aqira, a Scholarvox Books Scraper.')
    parser.add_argument('-id', '--docid', type=int, help='Book ID')
    parser.add_argument('-l', '--lower', type=int, help='Lower bound for Pages', default=1)
    parser.add_argument('-u', '--upper', type=int, help='Upper bound for Pages', default=15)
    parser.add_argument('-o', '--output', type=str, help='Output PDF name', default='output.pdf')
    parser.add_argument('-s', '--square', type=bool, help='Square Book Layout', default=False)
    args = parser.parse_args()
    return (args.docid, args.lower, args.upper, args.output, args.square)

def getDriver():
    try:
        s = Service(ChromeDriverManager().install()) 
        config = webdriver.ChromeOptions() 
        config.add_argument('--disable-infobars')
        config.add_argument('--incognito')
        config.add_experimental_option('excludeSwitches', ['enable-automation'])
        config.add_experimental_option('useAutomationExtension', False)
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        config.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(service=s, options=config)
        driver.get('https://google.com')
        #driver.maximize_window()
        driver.set_window_size(H,W)
        dim = driver.get_window_size() # Map return 
        return (driver, dim)
    except:
        exit('Driver Error')

def siteAuth(driver):
    driver.get('https://international.scholarvox.com/login/')
    driver.find_element(By.XPATH, '/html/body/div[8]/div[2]/form/p[1]/input').send_keys(USERNAME)
    driver.find_element(By.XPATH, '/html/body/div[8]/div[2]/form/p[2]/input').send_keys(PASSWORD)
    driver.find_element(By.XPATH, '/html/body/div[8]/div[2]/form/input[2]').click()
    print(Fore.GREEN + 'Authentification Done!')

# Task: Define Auth interval, Fix Cropping and improve timing
def scrapeContent(driver, docid, lower, upper, output, SQ=False):
    URL = 'https://international.scholarvox.com/reader/docid/%s/page/' % str(docid)
    # Creating images directory
    if not os.path.isdir('images'):
        print(PATH)
        try:
            os.mkdir(PATH + '\images')
        except OSError:
            print(Fore.RED + 'ERROR: Creation of directory Failed!', file=sys.stderr)
        else:
            print(Fore.GREEN + 'Successfully created images directory')

    t0 = datetime.datetime.now().minute
    siteAuth(driver)
    pdf = FPDF(unit='mm')

    try:
        auth_stack = []
        for i in range(lower, upper+1):
            name = 'Page%04d' % i 
            driver.get('%s%d' % (URL, i))
            time.sleep(5)
            driver.find_element(By.XPATH, '/html/body/div[4]/a[4]').click()
            png = driver.get_screenshot_as_png()
            img = Image.open(io.BytesIO(png)) 
            if SQ:
              img = img.crop(SQ_CROP)
            else:
              img = img.crop(A4_CROP)
            img.save(r'%s\images\%s.png' % (PATH, name))
            W,H = img.size
            W,H = float(W * 0.264583), float(H * 0.264583)
            pdf.add_page(format=(W, H))
            pdf.image(r'%s\images\%s.png' % (PATH, name), 0, 0, W, H)
            print(Fore.GREEN + '[Finished %s]' % name)
            # Reauthentificate every 20 minutes
            t1 = datetime.datetime.now().minute
            if t1-t0 == 20 and not auth_stack[-1]:
                siteAuth(driver)
                auth_stack.append(True)
        pdf.output(name=output, dest='F')
    finally:
        driver.close()
        driver.quit()

def main():
    DOCID, LOWER, UPPER, OUTPUT, SQ= parseArguments()
    DRIVER, DIM = getDriver()
    scrapeContent(DRIVER, DOCID, LOWER, UPPER, OUTPUT, SQ)
    
if __name__ == '__main__':
    main()
    sys.exit(0)
