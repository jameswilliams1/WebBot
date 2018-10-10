from selenium import webdriver
from time import sleep
from random import randrange, choice
from selenium.common.exceptions import StaleElementReferenceException, InvalidSelectorException, ElementNotVisibleException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from threading import Thread, Event
import string


site = ""
target = ""
max_threads = 0
min_time = 0
max_time = 0
active_threads = 0
proxy_type = ""
chrome_options = webdriver.ChromeOptions()
proxy_list = []
windows = True
script = []
min_pause_time = 0
max_pause_time = 0
scroll_count = 0
key_to_press = ""
click_count = 0
id_of_elements = []
class_of_elements = []


def rand(min_time, max_time):
    """
    Returns random time interval between min and max seconds to 3 d.p.
    :param min_time:
    :param max_time:
    :return: time:
    """
    return min_time + randrange(0, (max_time-min_time) * 1000) / 1000


def get_non_links(driver, address):
    actions = ActionChains(driver)
    # Find elements in body that have an ID
    driver.get(address)
    elements_with_id = driver.find_elements_by_xpath("//body//*[@id]")
    elements_ids = []
    same_page_ids = []
    for e in elements_with_id:
        elements_ids.append(e.get_attribute('id'))
    # Remove duplicates
    elements_ids = list(set(elements_ids))
    for e_id in elements_ids:
        try:
            # Following sequence will fail if page changes
            e = driver.find_element_by_id(e_id)
            actions.move_to_element(e)
            e.click()
            sleep(rand(1, 2))
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            sleep(rand(1, 2))
            e.click()
            sleep(rand(1, 2))
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            same_page_ids.append(e.get_attribute('id'))
        except StaleElementReferenceException:
            driver.execute_script("window.history.go(-1)")
            sleep(rand(2, 3))
        except (ElementNotVisibleException, WebDriverException):
            pass
    driver.get(address)
    # Find links with a class
    links = driver.find_elements_by_xpath('//body//a[@class]')
    link_class = []
    for e in links:
            link_class.append(e.get_attribute('class'))
    link_class = list(set(link_class))
    same_page_link_class = []
    for this_class in link_class:
        try:
            element = driver.find_element_by_class_name(this_class)
            actions.move_to_element(element)
            element.click()
            sleep(rand(1, 2))
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            element.click()
            sleep(rand(1, 2))
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            same_page_link_class.append(this_class)
        except StaleElementReferenceException:
            driver.execute_script("window.history.go(-1)")
            sleep(rand(2, 3))
        except (ElementNotVisibleException, WebDriverException):
            pass
        driver.close()
        global id_of_elements, class_of_elements
        id_of_elements = same_page_ids
        class_of_elements = same_page_link_class


def scroll_up(driver, count):
    """Scrolls up/down with random waits to random (within range) locations count times.
    :param driver:
    :param count:
    """
    for i in range(0, count):
        sleep(rand(2, 5))
        driver.execute_script("window.scrollTo(0,%d);" % rand(0, 200))
        print("Scrolled up")


def scroll_down(driver, count):
    """Scrolls up/down with random waits to random (within range) locations count times.
    :param driver:
    :param count:
    """
    for i in range(0, count):
        sleep(rand(2, 5))
        driver.execute_script("window.scrollTo(0,%d);" % rand(2000, 5000))
        print("Scrolled down")


def press_key(driver):
    global key_to_press, non_link_elements
    sleep(rand(2, 5))
    target_element = choice(non_link_elements)
    driver.find_element_by_xpath().send_keys(key_to_press)
    print("Pressed %d key" % key_to_press)


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
    sleep(rand(2, 5))
    try:
        target = driver.find_element_by_xpath(xpath)
        target.click()
        print("Clicked target element: " + xpath)
    except InvalidSelectorException as e:
        print("Failed to click target element:")
        print(e)


def random_actions(driver, max_count):
    """Pick a random function and run it with a random 1-3 count input a random amount of times between max_count and
    max_count/2"""
    functions = [click_random]
    for i in range(0, round(max_count/2) + randrange(0, round(max_count/2))):
        random_choice = choice(functions)
        random_choice(driver, randrange(1, 3))


def random_key():
    all_keys = string.ascii_letters + string.digits
    return choice(all_keys)


def set_parameters(min_pause_time_in, max_pause_time_in, scroll_count_in, key_press_in, click_count_in):
    global min_pause_time, max_pause_time, scroll_count, key_press, click_count, parameters_set
    min_pause_time = int(min_pause_time_in)
    max_pause_time = int(max_pause_time_in)
    scroll_count = int(scroll_count_in)
    key_press = str(key_press_in)
    click_count = int(click_count_in)
    print(min_pause_time, max_pause_time, scroll_count, key_press, click_count)


def update_script(new_script):
    global script
    script.clear()
    script = list(filter(lambda x: x != 'none', new_script))


def show_windows(new_status):
    global windows
    windows = new_status


def update_site(new_site):
    global site
    site = new_site


def update_target(new_target):
    global target
    target = new_target


def update_threads(new_count):
    global max_threads
    max_threads = new_count


def update_min(new_min):
    global min_time
    min_time = new_min


def update_max(new_max):
    global max_time
    max_time = new_max


def update_proxy(new_proxy):
    global proxy_type
    proxy_type = new_proxy


def clear_proxy():
    chrome_options.arguments.clear()
    proxy_list.clear()


def change_proxy(ip, port):
    clear_proxy()
    proxy_arg = ip + ":" + str(port)
    chrome_options.add_argument('--proxy-server=%s' % proxy_arg)


def make_proxy_list(filepath):
    clear_proxy()
    global proxy_list
    with open(filepath) as f:
        address_list = f.read().splitlines()
    proxy_list = ['--proxy-server=%s' % p for p in address_list]


class Worker(Thread):
    address = site
    xpath = target

    def __init__(self, options):
        super(Worker, self).__init__()
        self._stop_event = Event()
        self.options = options

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        print("Bot started on page: " + site)
        driver = webdriver.Chrome(chrome_options=self.options)
        driver.get(site)
        # driver.maximize_window()
        sleep(100)
        sleep(rand(5, 10))
        #random_actions(driver, 15)
        # click_target(driver, target)
        #random_actions(driver, 6)
        #sleep(rand(5, 10))
        driver.close()
        global active_threads
        active_threads -= 1
        print("Success: Closed browser.")


def run_threads():
    global active_threads
    active_threads = 0
    if not windows:
        chrome_options.add_argument("--headless")
    while 1:
        if len(proxy_list) == 0 and active_threads < max_threads:
            thread = Worker(chrome_options)
            thread.start()
            active_threads += 1
            print(str(active_threads) + " bots are active")
        elif len(proxy_list) != 0 and active_threads < max_threads:
            for p in proxy_list:
                chrome_options.arguments.clear()
                chrome_options.add_argument(p)
                if not windows:
                    chrome_options.add_argument("--headless")
                while active_threads == max_threads:
                    sleep(5)
                thread = Worker(chrome_options)
                thread.start()
                active_threads += 1
                print(str(active_threads) + " bots are active")
        else:
            sleep(10)





