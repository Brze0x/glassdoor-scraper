import re
import json
import logging
from typing import Union
from common import Common


logging.basicConfig(filename='employer_logs.log',
                    filemode='a',
                    format='%(asctime)s %(message)s', 
                    datefmt='%d.%m.%Y %H:%M:%S',
                    level=logging.INFO,
                    encoding='utf-8'
                    )

class Employers:
    def __init__(self) -> None:
        self.pattern = r"({\"id\":\d+,\"name\":.*?})\}\){1,}"
        self.employers = {"employers":[], "problemPages": []}
        self.url = 'https://www.glassdoor.com/Reviews/index.htm'

    def sort_list_of_dicts(self, lst: list, key: str) -> list[dict]:
        return sorted(lst, key=lambda i: i[key])

    def normalize_data(self, data: str) -> str:
        script = re.sub(r"\\{2,}\"", r"'", data)
        return re.sub(r"\\{1}", r"", script)

    def get_missing_data(self, what: list, where: list) -> list:
        return [item for item in what if item not in where]

    def get_employers_lst(self, pattern: str, script: str) -> list: 
        return [json.loads(employer) for employer in re.findall(pattern, script)[::2]]

    def get_employers_from_pages(self, start: int, stop: int, logs: bool=False) -> dict[str, list]:
        for i in range(start, stop):
            params = {"overall_rating_low": 3, "page": i}
            content = Common.get_page_content(url=self.url, params=params)
            if content[-1] >= 500:
                break
            lst = self.get_employers_lst(self.pattern, self.normalize_data(Common.get_script_tag_data(content[0])))
            if logs and len(lst) != 10:
                logging.info(f'Current page: {i}')
                logging.info(f'Length employers_lst: {len(lst)}')
                self.employers['problemPages'].append(i)
            for item in lst:
                self.employers["employers"].append(item)
        return self.employers

    def get_employers_from_problem_pages(self, pages: list, logs: bool=False) -> Union[dict[str, list], list]:
        if not pages:
            return []
        for page in pages:
            params = {"overall_rating_low": 3, "page": page}
            content = Common.get_page_content(url=self.url, params=params)
            if content[-1] >= 500:
                break
            lst = self.get_employers_lst(self.pattern, self.normalize_data(Common.get_script_tag_data(content[0])))
            if logs and len(lst) != 10:
                logging.info(f'Current page: {page}')
                logging.info(f'Length employers_lst: {len(lst)}')
            self.employers["employers"] += self.get_missing_data(lst, self.employers["employers"])
        return self.employers
