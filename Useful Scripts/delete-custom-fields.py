import mysql.connector

def get_db_prefix():
	db_prefix = 'wp_'
	return db_prefix

def get_my_db():
	my_db = mysql.connector.connect(
	  host = 'localhost',
	  user = 'root',
	  password = 'root',
	  unix_socket = 'mysqld.sock',
	  database = 'local',
	)
	return my_db

def delete_dt_field_customizations():
	global config
	my_db = get_my_db()
	my_cursor = my_db.cursor()
	db_prefix = get_db_prefix()
	my_cursor.execute("DELETE FROM `%soptions` WHERE option_name = 'dt_field_customizations' OR option_name = 'dt_custom_tiles';" % db_prefix)
	my_db.commit()
	print(' - [DT Field Customizations deleted successfully]')

delete_dt_field_customizations()