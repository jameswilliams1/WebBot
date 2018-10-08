from selenium import webdriver
from time import sleep
from random import randrange
from random import choice
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidSelectorException


def rand(min_time, max_time):
    """
    Returns random time interval between min and max seconds to 3 d.p.
    :param min_time:
    :param max_time:
    :return: time:
    """
    return min_time + randrange(0, (max_time-min_time) * 1000) / 1000


def find_all(driver):
    """Gets all elements of page inside body that aren't scripts or styles"""
    body_children = driver.find_elements_by_xpath("//body//*")
    body_children = filter(lambda element: element.tag_name != "style" and element.tag_name != "script", body_children)
    return body_children


def scroll(driver, count):
    """Scrolls down and up with random waits to random (within range) locations count times.
    :param driver:
    :param count:
    """
    for i in range(0, count):
        sleep(rand(3, 10))
        driver.execute_script("window.scrollTo(0,%d);" % rand(500, 5000))
        print("Scrolled down")
        sleep(rand(3, 10))
        driver.execute_script("window.scrollTo(0,%d);" % rand(0, 200))
        print("Scrolled up")


def click_random(driver, count):
    """Clicks random elements until the page changes then goes back. Repeats for count times."""
    for i in range(0, count):
        elements = find_all(driver)
        for e in elements:
            try:
                e.click()
                print("Clicked " + e.tag_name)
                sleep(rand(2, 5))
            except StaleElementReferenceException:
                print("Page change")
                sleep(rand(3, 8))
                driver.execute_script("window.history.go(-1)")
                print("Went back")
                sleep(rand(2, 5))
                break
            except Exception:
                continue


def click_target(driver, xpath):
    """Finds and clicks a specific element by its XPath."""
    sleep(rand(3, 5))
    try:
        target = driver.find_element_by_xpath(xpath)
        target.click()
        print("Clicked target element: " + xpath)
    except InvalidSelectorException as e:
        print("Failed to click target element:")
        print(e)
    finally:
        sleep(rand(5, 10))


def random_actions(driver, max_count):
    """Pick a random function and run it with a random 1-3 count input a random amount of times between max_count and
    max_count/2"""
    functions = [scroll, click_random]
    for i in range(0, round(max_count/2) + randrange(0, round(max_count/2))):
        random_choice = choice(functions)
        random_choice(driver, randrange(1, 3))


site = ""
target = ""


def update_site(string):
    global site
    site = string


def update_target(string):
    global target
    target = string


def run():
    print("Bot started on page: " + site)
    print (site)
    print(target)
    driver = webdriver.Chrome()
    driver.get(site)
    # driver.maximize_window()
    sleep(rand(5, 10))
    random_actions(driver, 15)
    #click_target(driver, target)
    random_actions(driver, 6)
    sleep(rand(5, 10))
    driver.close()
    print("Success: Closed browser.")