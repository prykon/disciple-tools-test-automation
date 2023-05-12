from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from sty import fg, bg, ef, rs
import os
import random
import string
import time
import re
import configparser
import mysql.connector

def create_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--log-level=3");
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.implicitly_wait(5)
    
    #Uncomment below if you want to automatically position the window somewhere and change its size
    #driver.set_window_position(241, -979, windowHandle='current')
    # driver.set_window_size(1050, 957, windowHandle='current')
    #driver.maximize_window()
    return driver

def load_config():
    try:
        open('config.ini', 'r')
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config
    except:
        config = configparser.ConfigParser()
        config['DATABASE'] = {}
        database = config['DATABASE']
        database['host'] = 'localhost'
        database['user'] = 'root'
        database['password'] = 'root'
        database['unix_socket'] = 'mysqld.sock'
        database['database_name'] = 'local'
        config['DEFAULT'] = {}
        config['DEFAULT']['url'] = 'http://localhost:10089'
        config['DEFAULT']['wp_user'] = 'admin'
        config['DEFAULT']['wp_pass'] = 'admin'
        config['DEFAULT']['longest_output'] = '0'
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    return config

def get_db_prefix():
	db_prefix = 'wp_'
	return db_prefix

def get_my_db(config_database):
	my_db = mysql.connector.connect(
	  host = config_database['host'],
	  user = config_database['user'],
	  password = config_database['password'],
	  unix_socket = config_database['unix_socket'],
	  database = config_database['database_name'],
	)
	return my_db

def calculate_longest_output(message):
	global longest_output
	if len(message) > longest_output:
		longest_output = len(message)
		config = configparser.ConfigParser()
		config.read('config.ini')
		config['DEFAULT']['longest_output'] = str(longest_output)
		with open('config.ini', 'w') as config_file:
			config.write(config_file)

def get_space_chars(message):
	global longest_output
	space_chars = 0
	if len(message) < longest_output:
		space_chars = longest_output - len(message)
	return space_chars

def bolded(message):
	return '\033[1m%s\033[0m' % message

def highlight(text):
	return fg.white + text + fg.rs

def wait_until_load():
	global driver
	WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

def scroll_to_top():
	driver.find_element(By.XPATH, '//body').send_keys(Keys.CONTROL + Keys.HOME)


def test_passed():
	ok_text = ' [%sOK%s]' % ( fg.green, fg.rs)
	print(f"{ok_text : >20}")


def test_not_passed(message=''):
	if message != '':
		message = ' - (%s)' % message
	error_text = ' [%serror%s] %s' % (fg.red, fg.rs, message)
	print(f"{error_text : >20}")


def random_string(chars=5):
	return str(''.join(random.choices(string.ascii_uppercase + string.digits, k=chars)))

def login(username, password):
	global driver, config
	wait_until_load()
	send_message('Log in')
	try:
		driver.find_element('id', 'user_login').send_keys(username)
		driver.find_element('id', 'user_pass').send_keys(password)
		driver.find_element('id', 'wp-submit').click()
		test_passed()
	except:
		test_not_passed('Login failed; shutting down.')
		exit()

def send_message(message, indent=0):
	global longest_output
	indentation = ' - '
	if indent > 0:
		indentation = '\t' * indent + '└ '
	message = indentation + message
	space_chars = get_space_chars(message)
	output = message + ' ' * space_chars
	print(output, end='')
	calculate_longest_output(output)

def refresh_page():
	driver.refresh()
	print('*** Page refreshed ***')


def test_click(message, xpath, indent=0):
	send_message(message, indent)
	try:
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
		driver.find_element(By.XPATH, xpath).click()
		test_passed()
	except:
		test_not_passed()

def test_click_random_from(message, xpath, indent=0):
	send_message(message, indent)
	try:
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
		elements = driver.find_elements(By.XPATH, xpath)
		random_element = random.choice(elements)
		random_element.click()
		test_passed()
		return random_element
	except:
		test_not_passed()

def test_visibility(message, xpath, indent=0):
	send_message(message, indent)
	try:
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
		element = driver.find_element(By.XPATH, xpath)
		if element.is_displayed():
			test_passed()
		else:
			test_not_passed()
	except:
		test_not_passed('Could not verify visibility')

def test_send_keys(message, xpath, keys, indent=0):
	wait_until_load()
	send_message(message, indent)
	try:
		driver.find_element(By.XPATH, xpath).send_keys(keys)
		test_passed()
	except:
		print(xpath)
		test_not_passed()

def test_element_present(message, xpath, indent=0):
	send_message(message, indent)
	try:
		time.sleep(1)
		driver.find_element(By.XPATH, xpath)
		test_passed()
	except:
		test_not_passed()

def test_element_not_present(message, xpath, indent=0):
	send_message(message, indent)
	try:
		time.sleep(1)
		driver.find_element(By.XPATH, xpath)
		test_not_passed()
	except:
		test_passed()

def test_checkbox_checked(message, xpath, indent=0):
	send_message(message, indent)
	if driver.find_element(By.XPATH, xpath).is_selected():
		test_passed()
	else:
		test_not_passed()

def test_element_attribute_matches(message, xpath, attribute, needle, indent=0):
	send_message(message, indent)
	try:
		element = driver.find_element(By.XPATH, xpath)
		if element.get_attribute(attribute) == needle:
			return True
	except:
		return False

def go_to_contacts_page(indent=0):
	send_message('Go to contacts page', True)
	try:
		global hostname
		driver.get( hostname + '/contacts')
		wait_until_load()
		test_passed()
	except:
		test_not_passed()

def select_random_contact_from_contacts_page(indent=0):
	send_message('Select random contact from contacts page', indent)
	try:	
		global driver
		contact_links_object = driver.find_elements(By.XPATH, "//tr[@class='dnd-moved']")
		contact_links = []
		for clo in contact_links_object:
			contact_links.append(clo.get_attribute('data-link'))
		random_contact_url = random.choice(contact_links)
		driver.get(random_contact_url)
		wait_until_load()
		test_passed()
	except:
		test_not_passed()

def get_post_type():
	return driver.execute_script('return window.wpApiShare.post_type;')

def get_post_type_from_wp_admin():
	return driver.execute_script('return window.field_settings.post_type;')

def test_expand_tile_menu(menu_id, indent=0):
	send_message("Testing %s tile menu expansion" % (highlight(menu_id)), indent)
	try:
		time.sleep(1)
		test_click("Test %s tile menu expand" % (highlight(t)), "//div[contains(@class, 'field-settings-table-tile-name') and @data-key='%s']" % menu_id, True)
		test_passed()
	except:
		test_not_passed()

	try:
		time.sleep(1)
		test_visibility( "Test %s tile submenu visibility" % (highlight(t)), "//div[contains(@class, 'tile-rundown-elements') and @data-parent-tile-key='%s']" % menu_id, True)
		test_passed()
	except:
		test_not_passed()

def get_all_field_types():
	global driver
	all_field_types = []
	driver.find_element(By.XPATH, "//div[contains(@class, 'field-settings-table-tile-name')]").click()
	driver.find_element(By.XPATH, "//span[@class='add-new-field']/a").click()
	time.sleep(1)
	field_types = driver.find_elements(By.XPATH, "//select[@name='new-field-type']/option")
	for ft in field_types:
		all_field_types.append(ft.get_attribute('value'))
	driver.find_element(By.XPATH, "//div[@class='dt-admin-modal-box-close-button']").click()
	driver.find_element(By.XPATH, "//div[contains(@class, 'field-settings-table-tile-name')]").click()
	return all_field_types

### DATABASE FUNCTIONS - START ###	
def delete_dt_field_customizations():
	global config
	my_db = get_my_db(config['DATABASE'])
	my_cursor = my_db.cursor()
	db_prefix = get_db_prefix()
	my_cursor.execute("DELETE FROM `%soptions` WHERE option_name = 'dt_field_customizations';" % db_prefix)
	my_db.commit()
	print(' - [DT Field Customizations deleted successfully]')
### DATABASE FUNCTIONS - END ###


# ==================================== #
#   START CUSTOM TESTING FUNCTIONS     #
# ==================================== #


driver = create_driver()
config = load_config()
longest_output = int(config['DEFAULT']['longest_output'])
driver.get(config['DEFAULT']['url'])
login(config['DEFAULT']['wp_user'], config['DEFAULT']['wp_pass'])
wait_until_load()
#driver.close()