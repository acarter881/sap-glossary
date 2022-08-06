import time
import re
from seleniumwire import webdriver

class Bearer:
    def __init__(self) -> None:
        self.url = 'https://help.sap.com/glossary/'
        self.driver_path = r'C:\Users\Alex\Desktop\Python drivers\chromedriver.exe'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    def bear(self) -> str:
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=self.options)
        self.driver.get(url=self.url)

        time.sleep(4)

        for request in self.driver.requests:
            if re.search(pattern=r'https:\/\/lx-fra-prod.+', string=str(request)):
                if request.headers['x-approuter-authorization']:
                    self.my_bearer = request.headers['x-approuter-authorization']

        return self.my_bearer

    def quit(self) -> None:
        self.driver.quit()