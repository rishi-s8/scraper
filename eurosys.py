from selenium import webdriver
import time
import csv

def getCredentials():
    file = open("credentials.txt", "r")
    data = file.readlines()
    userName = data[0].rstrip('\n')
    password = data[1].rstrip('\n')
    return userName, password

def get_options():
    binaryPath = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    options = webdriver.ChromeOptions()
    options.binary_location = binaryPath
    return options


if __name__ == "__main__":
    driver = webdriver.Chrome(options=get_options())
    driver.delete_all_cookies()
    time.sleep(3)
    driver.get("https://eurosys22.hotcrp.com/")
    userName, password = getCredentials()
    userField = "email"
    passwordField = "password"
    driver.find_element_by_name(userField).send_keys(userName)
    driver.find_element_by_name(passwordField).send_keys(password)
    driver.find_element_by_tag_name("form").submit()

    # Accepted Papers
    time.sleep(3)
    driver.get("https://eurosys22.hotcrp.com/search?q=&t=acc")
    accepted_papers = []
    contents = driver.find_elements_by_class_name('pl')
    for content in contents:
        id = content.get_attribute("id")
        if id != '':
            accepted_papers.append(id)
    
    # Accepted Users
    accepted_users = set()
    for ap in accepted_papers:
        time.sleep(3)
        driver.get("https://eurosys22.hotcrp.com/paper/{}".format(ap[1:]))
        contents=driver.find_elements_by_css_selector('.pg>.pavb>.fx9>.odname>a')
        for content in contents:
            mail = content.get_attribute("href")
            if mail.startswith("mailto:"):
                accepted_users.add(mail[7:])

        # break #TODO: Remove this

    infos = []
    for au in accepted_users:
        time.sleep(3)
        print("Opening User: ", au)
        driver.get("https://eurosys22.hotcrp.com/profile/{}/demographics".format(au))
        if driver.current_url.endswith("demographics"):
            infos.append({"email":au, "gender": "", "birth_year": ""})
            content = driver.find_element_by_id("gender")
            for option in content.find_elements_by_css_selector("*"):
                if option.get_attribute("selected"):
                    infos[-1]["gender"] = option.text
            
            value = driver.find_element_by_id("birthday").get_attribute("value")
            infos[-1]["birth_year"] = value

    print(infos)

    keys = infos[0].keys()
    with open('people.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(infos)

    driver.find_element_by_css_selector('#header-right > form').submit()
    time.sleep(3)
    driver.close()