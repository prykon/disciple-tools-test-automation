# Disciple.Tools Test Automation

This is a Python script that utilizes the Selenium WebDriver library to automate web browser interactions and perform tests on a the [Disciple.Tools WordPress theme](https://github.com/DiscipleTools/disciple-tools-theme). The script includes several custom functions for specific testing scenarios.

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Example Usage](#example-usage)
- [Functions](#functions)

## Prerequisites

- Python 3.x
- [Selenium WebDriver](https://www.selenium.dev/documentation/en/webdriver/)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)
- [MySQL Connector](https://pypi.org/project/mysql-connector-python/)
- [sty](https://pypi.org/project/sty/)

## Installation

1. Install the required dependencies by running the following command:
`pip install -r requirements.txt`

2. Download the appropriate ChromeDriver executable using WebDriver Manager:

```python
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
```

3. Configure the `config.ini` File

1. Open the `config.ini` file in a text editor.

2. Provide the MySQL database credentials in the `[DATABASE]` section:

```[DATABASE]
host = localhost
user = root
password = root
unix_socket = mysqld.sock
database_name = local
```

6. Set the web application URL, WordPress username, and password in the `[DEFAULT]` section:
```ini
[DEFAULT]
url = http://localhost:10089
wp_user = admin
wp_pass = admin
longest_output = 0
```
## Example Usage
In order to run a test, you must follow these steps.

1. Go to the `Test Cases` folder and select the test case you want.
2. Copy and paste the test case code at the bottom of the `main.py` file, where it says `Start Custom Testing Functions`
3. Execute your code by running the `main.py` file in a terminal window. The command that executes the code should be something along the lines of `python main.py` after navigating to the folder in the terminal, but this can vary.

## Functions
A detailed explanation of each function.
*Under Construction*