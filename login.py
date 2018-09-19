from selenium import webdriver
import time
chromeDriver = "./chromedriver"
driver = webdriver.Chrome(executable_path=chromeDriver)

def getCredentialsWebMail():
    file = open("credentialsWebMail.txt", "r")
    data = file.readlines()
    userName = data[0].rstrip('\n')
    password = data[1].rstrip('\n')
    return userName, password

def webMailLogin():
    userName, password = getCredentialsWebMail()
    userField = "_user"
    passwordField = "_pass"
    submitButton = "rcmloginsubmit"
    driver.get("https://students.iitmandi.ac.in/webmail/?_task=login")
    driver.find_element_by_name(userField).send_keys(userName)
    driver.find_element_by_name(passwordField).send_keys(password)
    driver.find_element_by_id(submitButton).click()

def getCredentialsLDAP():
    file = open("credentialsLDAP.txt", "r")
    data = file.readlines()
    userName = data[0].rstrip('\n')
    password = data[1].rstrip('\n')
    return userName, password

def gatewayLogin():
    userName, password = getCredentialsLDAP()
    userField = "username"
    passwordField = "password"
    driver.get("http://gateway.iitmandi.ac.in/facstaff/login.php")
    driver.find_element_by_name(userField).send_keys(userName)
    driver.find_element_by_name(passwordField).send_keys(password)
    driver.find_element_by_tag_name("form").submit()

gatewayLogin();
driver.close()
