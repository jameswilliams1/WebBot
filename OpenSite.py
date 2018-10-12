from selenium import webdriver
from time import sleep, time
from random import randrange, choice
from selenium.common.exceptions import StaleElementReferenceException, InvalidSelectorException, ElementNotVisibleException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
script_pre = []
min_pause_time = 0
max_pause_time = 0
scroll_count = 0
key_to_press = ""
click_count = 0
bot_count = 0
same_page_ids = []
same_page_class = []


def rand(min_time, max_time):
    """
    Returns random time interval between min and max seconds to 3 d.p.
    :param min_time:
    :param max_time:
    :return: time:
    """
    return min_time + randrange(0, (max_time-min_time) * 1000) / 1000


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class ListWorker(Thread):
    global site, same_page_ids, same_page_class

    def __init__(self, options, list_of_el, list_type):
        super(ListWorker, self).__init__()
        self.options = options
        self.list_of_el = list_of_el
        self.list_type = list_type

    def run(self):
        driver = webdriver.Chrome(chrome_options=self.options)
        driver.get(site)
        if self.list_type == 'id':
            for e_id in self.list_of_el:
                try:
                    e = driver.find_element_by_id(e_id)
                    ActionChains(driver).move_to_element(e)
                    e.click()
                    #print("clicked id %s" % e.get_attribute('id'))
                    sleep(rand(3, 5))
                    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                    WebDriverWait(driver, 6).until(EC.visibility_of(e))
                    e.click()
                    sleep(rand(3, 5))
                    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                    same_page_ids.append(e.get_attribute('id'))
                except StaleElementReferenceException:
                    driver.get(site)
                    sleep(rand(3, 5))
                except (ElementNotVisibleException, WebDriverException):
                    pass
        elif self.list_type == 'class':
            for this_class in self.list_of_el:
                try:
                    e = driver.find_element_by_class_name(this_class)
                    ActionChains(driver).move_to_element(e)
                    e.click()
                    #print("clicked class %s" % e.get_attribute('class'))
                    sleep(rand(3, 5))
                    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                    WebDriverWait(driver, 6).until(EC.visibility_of(e))
                    e.click()
                    sleep(rand(3, 5))
                    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                    same_page_class.append(this_class)
                except StaleElementReferenceException:
                    driver.get(site)
                    sleep(rand(3, 5))
                except (ElementNotVisibleException, WebDriverException):
                    pass
        driver.close()


def get_non_links(chrome_options):
    global site, same_page_class, same_page_ids
    same_page_class.clear()
    same_page_ids.clear()
    # Find elements in body that have an ID
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(site)
    #sleep(rand(4, 8))
    elements_with_id = driver.find_elements_by_xpath("//body//*[@id]")
    elements_ids = []
    for e in elements_with_id:
        try:
            elements_ids.append(e.get_attribute('id'))
        except StaleElementReferenceException:
            pass
    # Remove duplicates
    elements_ids = list(set(elements_ids))
    driver.get(site)
    # Find links with a class
    elements_with_class = driver.find_elements_by_xpath('//body//*[@class]')
    element_class = []
    for e in elements_with_class:
        try:
            element_class.append(e.get_attribute('class'))
        except StaleElementReferenceException:
            pass
    element_class = list(set(element_class))
    driver.close()
    split_id_list = chunks(elements_ids, 10)
    split_class_list = chunks(element_class, 10)
    thread_list = []
    for sub_id_list in split_id_list:
        thread = ListWorker(chrome_options, sub_id_list, 'id')
        thread.start()
        thread_list.append(thread)
    for sub_class_list in split_class_list:
        thread = ListWorker(chrome_options, sub_class_list, 'class')
        thread.start()
        thread_list.append(thread)
    for t in thread_list:
        t.join()


def scroll_up(driver, count):
    """Scrolls up/down with random waits to random (within range) locations count times.
    :param driver:
    :param count:
    """
    for i in range(0, count):
        sleep(rand(2, 5))
        driver.execute_script("window.scrollTo(0,%d);" % rand(0, 200))
    print("Scrolled up %d times" % count)


def scroll_down(driver, count):
    """Scrolls up/down with random waits to random (within range) locations count times.
    :param driver:
    :param count:
    """
    for i in range(0, count):
        sleep(rand(2, 5))
        driver.execute_script("window.scrollTo(0,%d);" % rand(2000, 5000))
    print("Scrolled down %d times" % count)


def press_key(driver):
    global key_to_press
    sleep(rand(2, 5))
    action = ActionChains(driver)
    action.send_keys(key_to_press).perform()
    print("Pressed %s key" % key_to_press)


def left_click(driver, count):
    """Clicks random element from random list, repeats for count times."""
    global site
    if len(same_page_ids) == 0 and len(same_page_class) == 0:
        print('No elements are present that can be clicked')
        return
    actions = ActionChains(driver)
    i = 0
    total_iter = 0
    while i < count:
        if total_iter >= count + 10:  # Break if too many fails
            print("Failed to complete all clicks")
            break
        sleep(rand(5, 8))
        list_choice = choice([same_page_ids, same_page_class])
        if len(same_page_ids) == 0:
            list_choice = same_page_class
        elif len(same_page_class) == 0:
            list_choice = same_page_ids
        if list_choice == same_page_ids:
            try:
                element = choice(same_page_ids)
                e = driver.find_element_by_id(element)
                actions.move_to_element(e)
                e.click()
                i += 1
                print("clicked ID %s" % element)
                sleep(rand(1, 2))
                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                try:
                    actions.move_to_element(e)
                except StaleElementReferenceException:
                    driver.get(site)
            except StaleElementReferenceException:
                if driver.current_url != site:
                    driver.get(site)
                pass
            except WebDriverException:
                pass
        elif list_choice == same_page_class:
            try:
                element = choice(same_page_class)
                e = driver.find_element_by_class_name(element)
                actions.move_to_element(e)
                e.click()
                i += 1
                print("clicked class %s" % element)
                sleep(rand(1, 2))
                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                try:
                    actions.move_to_element(e)
                except StaleElementReferenceException:
                    driver.get(site)
            except StaleElementReferenceException:
                if driver.current_url != site:
                    driver.get(site)
                pass
            except WebDriverException:
                pass
        total_iter += 1


def click_target(driver, xpath):
    """Finds and clicks a specific element by its XPath."""
    sleep(rand(2, 5))
    action = ActionChains(driver)
    if len(xpath) == 0:
        print("No XPath selected")
        return
    try:
        target_obj = driver.find_element_by_xpath(xpath)
        action.move_to_element(target_obj)
        target_obj.click()
        sleep(rand(2, 5))
        action.send_keys(Keys.ESCAPE).perform()
        print("Clicked target element: " + xpath)
    except (WebDriverException, StaleElementReferenceException, InvalidSelectorException) as e:
        print("Failed to click target element:")
        print(e)


def random_key():
    all_keys = string.ascii_letters + string.digits
    return choice(all_keys)


def set_parameters(min_pause_time_in, max_pause_time_in, scroll_count_in, key_press_in, click_count_in):
    global min_pause_time, max_pause_time, scroll_count, key_to_press, click_count
    min_pause_time = int(min_pause_time_in)
    max_pause_time = int(max_pause_time_in)
    scroll_count = int(scroll_count_in)
    key_to_press = str(key_press_in)
    click_count = int(click_count_in)


def update_script(new_script):
    global script_pre
    script_pre = list(filter(lambda x: x != 'none', new_script))


def process_script(driver):
    global script_pre
    script = []
    for i in script_pre:
        if i == 'sleep':
            script.append((sleep, rand(min_pause_time, max_pause_time)))
        elif i == 'scroll_up':
            script.append((scroll_up, driver, scroll_count))
        elif i == 'scroll_down':
            script.append((scroll_down, driver, scroll_count))
        elif i == 'press_key':
            script.append((press_key, driver))
        elif i == 'left_click':
            script.append((left_click, driver, click_count))
    return script


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
    global site, min_time, max_time, target, bot_count

    def __init__(self, options):
        super(Worker, self).__init__()
        self.options = options

    def run(self):
        try:
            start_time = time()
            bot_number = bot_count
            print("Bot %d started on page: " % bot_number + site)
            run_time = rand(min_time, max_time)
            xpath_time = int(run_time / 2) + rand(0, int(run_time / 6))
            driver = webdriver.Chrome(chrome_options=self.options)
            driver.get(site)
            sleep(rand(3, 5))
            script_list = process_script(driver)
            target_clicked = False
            while time() - start_time <= run_time:
                for t in script_list:
                    t[0](*t[1:])
                    if time() - start_time >= xpath_time and target_clicked is False:
                        click_target(driver, target)
                        target_clicked = True
        except Exception as e:
            print("Bot %d crashed with the following error:" % bot_number)
            print(e)
        finally:
            driver.close()
            global active_threads
            active_threads -= 1
            print("Closed browser")


def run_threads():
    global active_threads, site, same_page_ids, same_page_class, script_pre, bot_count
    bot_count = 1
    active_threads = 0
    j = 0
    if not windows:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument(
            "--user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'")
    print("Generating list of elements to click...")
    while j < 5:
        try:
            if len(proxy_list) != 0:
                chrome_options.arguments.clear()
                chrome_options.add_argument(proxy_list.index(j))
                if not windows:
                    chrome_options.add_argument("--headless")
                    chrome_options.add_argument('--disable-gpu')
                    chrome_options.add_argument("window-size=1920,1080")
                    chrome_options.add_argument(
                        "--user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'")
            get_non_links(chrome_options)
            break
        except Exception as e:
            print('There was a error while finding links to click:')
            print(e)
            if len(proxy_list) != 0:
                print("The issue is most likely with proxy #%d" % j + 1)
            if j == 4 or len(proxy_list) == 0:
                print("Could not find links to click, check proxy and website settings")
                break
        finally:
            j += 1
    if len(same_page_ids) + len(same_page_class) > 0:
        print('Finished. %d elements were found' % (len(same_page_ids) + len(same_page_class)))
    print("Starting threads...")
    while 1:
        if len(proxy_list) == 0 and active_threads < max_threads:
            thread = Worker(chrome_options)
            thread.start()
            active_threads += 1
            bot_count += 1
            print(str(active_threads) + " bots are active")
            sleep(4)
        elif len(proxy_list) != 0 and active_threads < max_threads:
            for p in proxy_list:
                chrome_options.arguments.clear()
                chrome_options.add_argument(p)
                if not windows:
                    chrome_options.add_argument("--headless")
                    chrome_options.add_argument('--disable-gpu')
                    chrome_options.add_argument("window-size=1920,1080")
                    chrome_options.add_argument("--user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'")
                while active_threads == max_threads:
                    sleep(10)
                thread = Worker(chrome_options)
                thread.start()
                active_threads += 1
                bot_count += 1
                print(str(active_threads) + " bots are active")
                sleep(4)
        else:
            sleep(10)
