# This test case makes sure that the new DT Customization settings are working correctly.
# Last tested on: DT Theme v.1.40.0

def get_post_type():
	return driver.execute_script('return window.wpApiShare.post_type;')

def get_post_type_from_wp_admin():
	return driver.execute_script('return window.field_settings.post_type;')

def test_expand_tile_menu(menu_id, indent=0):
	time.sleep(1)
	test_click("Test %s tile menu expand" % (highlight(t)), "//div[contains(@class, 'field-settings-table-tile-name') and @data-key='%s']" % menu_id, True)
	time.sleep(1)
	test_visibility( "Test %s tile submenu visibility" % (highlight(t)), "//div[contains(@class, 'tile-rundown-elements') and @data-parent-tile-key='%s']" % menu_id, True)

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

def delete_dt_field_customizations():
	global config
	my_db = get_my_db(config['DATABASE'])
	my_cursor = my_db.cursor()
	db_prefix = get_db_prefix()
	my_cursor.execute("DELETE FROM `%soptions` WHERE option_name = 'dt_field_customizations';" % db_prefix)
	my_db.commit()
	print(' - [DT Field Customizations deleted successfully]')



driver = create_driver()
config = load_config()
delete_dt_field_customizations()
longest_output = int(config['DEFAULT']['longest_output'])
driver.get(config['DEFAULT']['url'] + '/wp-admin/admin.php?page=dt_customizations&post_type=contacts&tab=tiles')
login(config['DEFAULT']['wp_user'], config['DEFAULT']['wp_pass'])
wait_until_load()


# Test tile menus collapse and expand
print()
send_message("Test tile menus expansion and collapse\n")
tiles = driver.execute_script("return window.field_settings.post_type_tiles;")
tiles = tiles.keys()

fields = driver.execute_script("return window.field_settings.post_type_settings.fields;")
all_field_types = get_all_field_types()

for t in tiles:
	time.sleep(2)
	test_expand_tile_menu(t, True)

	# Test add new field for all field types
	for aft in all_field_types:
		if aft == 'connection':
			continue
		send_message("Test adding a new '%s' field in %s tile\n" % (highlight(aft), highlight(t)), 1)
		test_click("Click %sadd new field%s link " % (fg.white, fg.rs), '//span[@class="add-new-field" and @data-parent-tile-key="%s"]' % t, 2)
		time.sleep(1)
		random_field_name = 'Random %s field %s' % (aft, random_string())
		random_field_key = random_field_name.replace(' ', '_').lower()
		test_send_keys("Write %s in input box" % highlight('new field name'), '//input[@name="edit-tile-label"]', random_field_name, 2)
		time.sleep(1)
		send_message("Select %s from field type dropdown" % (highlight(aft)), 2)
		field_type_dropdown = Select(driver.find_element(By.XPATH, '//select[@name="new-field-type"]'))
		field_type_dropdown.select_by_value(aft)
		print()
		test_click("Test Save button click", '//button[@id="js-add-field"]' , 2)
		print()
		test_element_present('Test %s field was created correctly' % highlight(random_field_key), '//div[contains(@class, "field-settings-table-field-name") and @data-key="%s" and @data-parent-tile-key="%s"]' % (random_field_key, t))

		# Test name field is editable
		send_message("Test %s field is editable\n" % highlight(random_field_name), 1)
		test_click("Test click edit icon", '//div[contains(@class, "field-settings-table-field-name") and @data-key="%s"]/span[@class="edit-icon"]' % (random_field_key), 1)
		#print('//div[contains(@class, "field-settings-table-field-name") and @data-key="%s"]/span[@class="edit-icon"]' % random_field_key)
		time.sleep(1)
		test_visibility("Testing if edit modal opened correctly.", '//div[contains(@class, "dt-admin-modal-box")]', 1)
		random_field_name_new = random_field_name + ' edited'
		driver.find_element(By.XPATH, '//input[@name="edit-field-custom-name"]').clear()
		test_send_keys("Writing new field name", '//input[@name="edit-field-custom-name"]', random_field_name_new, 1)
		test_click("Test Save button click", '//button[@id="js-edit-field"]' , 1)
		send_message("Test %s field was edited correctly" % highlight(random_field_name), 1)
		try:
			time.sleep(1)
			actual_field_name = driver.find_element(By.XPATH, '//span[@class="field-name-content" and @data-key="%s" and @data-parent-tile="%s"]' % (random_field_key, t)).text.strip()
			if actual_field_name == random_field_name_new:
				test_passed()
			else:
				test_not_passed()
		except:
			test_not_passed()
		

	# Test expanding each field menu
	for fk, fv in fields.items():
		if 'tile' in fv and fv['tile'] == t and 'default' in fv and fv['default']:
			test_click("Test %s > %s field menu expand" % (highlight(t), highlight(fk)), "//div[contains(@class, 'field-settings-table-field-name') and contains(@class, 'expandable') and @id='%s']" % fk, 2)
			time.sleep(1)
			test_visibility( "Test %s > %s field submenu visibility" % (highlight(t), highlight(fk)), "//*[@id='%s']//*[contains(@class, 'field-settings-table-child-toggle')]" % fk, 2)

driver.close()