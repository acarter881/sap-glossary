import requests
import json
import pandas as pd
import concurrent.futures
from bearer import Bearer

class Glossary:
    def __init__(self) -> None:
        # Dictionary to store each term and its definition
        self.terms = dict()
        # Get this from https://help.sap.com/glossary/ | this value changes every 15-30 minutes. Using an invalid authorization will not generate results
        the_bear = Bearer()
        self.x_approuter_authorization = the_bear.bear()
        the_bear.quit()
        print('Bearer acquired!')
        # Headers for each GET request
        self.headers = {
                        'accept': 'application/json',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'en-US,en;q=0.9',
                        'referer': 'https://help.sap.com/',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                        'x-approuter-authorization': self.x_approuter_authorization,
                       }

    def get_terms(self, pg_num: int) -> None:
        print(f'Requesting data from page {pg_num}')

        url = f'https://lx-fra-prod-app-route-term-api.cfapps.eu10.hana.ondemand.com/glossary/lookup?language=en-US&retired=false&glossaryPresent=Entries_With_Definitions&status=Released&online=Public_Entries&objectType=Main_Entry&pageSize=50&pageNo={pg_num}'

        r = requests.get(url=url, headers=self.headers)

        the_json = json.loads(s=r.text)

        if the_json['matches']:
            for match in the_json['matches']:
                self.terms[match['term']] = [match['definition'], match['component'], match['componentLongForm']]
        
    def to_pandas(self) -> None:
        df = pd.DataFrame.from_dict(data=self.terms, orient='index', columns=['Definition', 'Component', 'Component-Long-Form'])
        df.to_excel(excel_writer='terms.xlsx', sheet_name='Terms', freeze_panes=(1,0))

    def my_threads(self) -> None:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.get_terms, range(1, 1500, 1))

# Run the necessary functions
if __name__ == '__main__':
    c = Glossary()
    c.my_threads()
    c.to_pandas()