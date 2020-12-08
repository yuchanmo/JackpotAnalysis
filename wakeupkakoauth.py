from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time




kakao_auth_url = 'http://114.203.39.76:9999/Home/code'
id = 'densetsu@nate.com'
pwd = 'ahdbapwk55'

def isLoginPage(u:str):
    login_url ='https://accounts.kakao.com/login?'
    return login_url in u


driver = Chrome(r'D:\Programming\stocktrading\trendanalyzer\chromedriver.exe')
driver.get(kakao_auth_url)
loginpage = isLoginPage(driver.current_url)

if loginpage:
    idtag = driver.find_element_by_id('id_email_2')
    idtag.clear()
    idtag.send_keys(id)
    pwdtag = driver.find_element_by_id('id_password_3')
    pwdtag.clear()
    pwdtag.send_keys(pwd)
    btn = driver.find_element_by_class_name('submit')
    btn.click()


time.sleep(10)
driver.close()