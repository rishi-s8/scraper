from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time

import json

newServer = "" # For example "https://confxyz.hotcrp.com/"

oldServerJSON = "" # Path to the JSON of details downloaded from HotCrp. For example "./confxyz-fall-data.json"
oldServerPDFDir = "" # Path to the directory where the PDFs are stored. For example "./pdfs"


def getCredentials():
    file = open("./credentials.txt", "r")
    data = file.readlines()
    userName = data[0].rstrip('\n')
    password = data[1].rstrip('\n')
    return userName, password

def get_options():
    # Binary path for Chrome or chromedriver
    binaryPath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    #binaryPath = './chromedriver'
    options = webdriver.ChromeOptions()
    options.binary_location = binaryPath
    return options


if __name__ == "__main__":
    driver = webdriver.Chrome(options=get_options())
    driver.delete_all_cookies()
    time.sleep(3)
    assert newServer != "", "Please provide the new server URL"
    driver.get(newServer)
    userName, password = getCredentials()
    userField = "email"
    passwordField = "password"
    driver.find_element_by_name(userField).send_keys(userName)
    driver.find_element_by_name(passwordField).send_keys(password)
    driver.find_element_by_tag_name("form").submit()



    diction = []
    assert oldServerJSON != "", "Please provide the path to the JSON file"
    with open(oldServerJSON, 'r') as f:
        json_data = f.read()
        diction = json.loads(json_data)




    for elems in diction:
        time.sleep(3)
        driver.get(f"{newServer}/paper/new")

        driver.find_element_by_name("title").send_keys(elems["title"])
        driver.find_element_by_name("abstract").send_keys(elems["abstract"])
        i = 1
        for author in elems["authors"]:
            time.sleep(1)
            driver.find_element_by_name("authors:email_{}".format(i)).clear()
            driver.find_element_by_name("authors:email_{}".format(i)).send_keys(author["email"])
            time.sleep(1)
            driver.find_element_by_name("authors:name_{}".format(i)).clear()
            driver.find_element_by_name("authors:name_{}".format(i)).send_keys(author["first"] + " " + author["last"])
            time.sleep(1)
            driver.find_element_by_name("authors:affiliation_{}".format(i)).clear()
            driver.find_element_by_name("authors:affiliation_{}".format(i)).send_keys(author["affiliation"])
            i+=1
        my_topics = set(elems["topics"])
        print(my_topics)
        fieldset = driver.find_element_by_name("topics")
        outer_elements = fieldset.find_elements_by_css_selector('label')
        print("Length: " + str(len(outer_elements)))
        for topics in outer_elements:
            inner = topics.get_attribute('innerHTML')
            topic_name = inner.split(">")[-1]
            if topic_name in my_topics:
                topics.find_elements_by_css_selector("input")[0].click()
        driver.find_element_by_name("opt9").click()
        driver.find_element_by_id("collaborators").send_keys(elems["collaborators"])

        submission_element = driver.find_elements_by_class_name("has-document")[0]
        print("Submission_element: {}".format(submission_element.get_attribute('innerHTML')))
        

        driver.execute_script("arguments[0].innerHTML = '<div class=\"document-upload\"><input id=\"submission\" type=\"file\" name=\"submission\" accept=\"application/pdf\" class=\"uich document-uploader\"></div><div class=\"document-actions\"><a href=\"\" class=\"ui js-cancel-document document-action\">Cancel</a></div><div class=\"document-replacer\"><button type=\"button\" class=\"ui js-replace-document\" id=\"submission:upload\">Upload</button></div>'", submission_element)

        time.sleep(7)
        submission_button = driver.find_element_by_name("submission")
        submission_button.send_keys(f'{oldServerPDFDir}/{elems["submission"]["content_file"]}')

        driver.find_elements_by_class_name("btn-savepaper")[0].click()

        time.sleep(15)

    time.sleep(3)
    driver.close()