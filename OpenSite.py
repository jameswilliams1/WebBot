from selenium import webdriver
from time import sleep
from random import randrange, choice
from selenium.common.exceptions import StaleElementReferenceException, InvalidSelectorException
from threading import Thread, Event


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
max_threads = 1
active_threads = 0
min_time = 0
max_time = 0
proxy_type = ""
chrome_options = webdriver.ChromeOptions()
proxy_list = []
windows = True


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





