from time import sleep
from selenium import webdriver
from urllib import request 
import traceback

AVERAGEPOSTHEIGHT = 925.0
N_OBTAINABLE = 6
SCROLLHEIGHT = AVERAGEPOSTHEIGHT * N_OBTAINABLE
brower = None

def scrollDown():
    # browser.execute_script("window.scrollTo(0, {0})".format(SCROLLHEIGHT)) 
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight*0.8)")
    sleep(3)

def loadCredential():
    f = open("credential.txt","r")
    cred = list(filter(None, f))
    return cred[0], cred[1]

def clickNotNow():
    if browser.find_elements_by_xpath("//*[contains(text(), 'Not Now')]"):
        browser.find_elements_by_xpath("//*[contains(text(), 'Not Now')]")[0].click()

def login():
    username , password = loadCredential()

    # login_link = browser.find_element_by_xpath("//a[text()='Log in']")
    # login_link.click()

    sleep(2)


    browser.get('https://www.instagram.com/')

    username_input = browser.find_element_by_css_selector("input[name='username']")
    password_input = browser.find_element_by_css_selector("input[name='password']")

    username_input.send_keys(username)
    password_input.send_keys(password)

    login_button = browser.find_element_by_xpath("//button[@type='submit']")
    login_button.click()

    # Logged in
    clickNotNow()
    sleep(1)
    clickNotNow()

def scrape_image():
    CYCLE = 6
    images = browser.find_elements_by_tag_name('img')    
    return filterImage(list(filter(None, images)))

def filterImage(collected=[]):
    if len(collected) < 1:
        raise "No Image found"
    
    result = []
    for image in collected:
        if int(image.size['width']) == 600:
            result.append(image)
    return result


def app():
    login()
    
    # Feed page
    CYCLE = 6
    index = 0
    for time in range(CYCLE):
        images = scrape_image()
        print('Image retrieved')    
        for img in images:
            fname = 'downloads/' + 'image_' +  str(index)+'.jpg'
            print('file name : {0}'.format(fname))
            request.urlretrieve(img.get_attribute('src'), fname)
            index +=1
        scrollDown()



if __name__ == "__main__":
    try:
        browser = webdriver.Chrome()
        browser.implicitly_wait(5)
        app()
    except Exception as e: 
        traceback.print_exc()
    finally:
        print('Success execution')
        browser.close()