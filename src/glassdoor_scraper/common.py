import json
import csv
import logging
import requests
from typing import Any
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry


class Common:
    @staticmethod
    def get_page_content(url: str, params: dict=None) -> tuple[str, int]:
        headers = {'user-agent': 'Chrome/108.0.0.0'}
        with requests.Session() as session:
            session.headers.update(headers)
            retry = Retry(connect=3, backoff_factor=5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            session.max_redirects = 60
            response = session.get(url=url, params=params, stream=True)
            return response.text, response.status_code

    @staticmethod
    def get_script_tag_data(content: str) -> str:
        return [s.text for s in BeautifulSoup(content, "lxml").find_all("script") if "window.appCache" in s.text][0]

    @staticmethod
    def remove_duplicates(lst: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [dict(t) for t in {tuple(d.items()) for d in lst}]

    @staticmethod
    def save_to_json(data: dict, file_name: str) -> None:
        with open(f'output/{file_name}.json', mode='w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def save_to_csv(data: list, file_name: str) -> None:
        with open(f'output/{file_name}.csv', mode='a', encoding="utf-8") as f:
            writer = csv.writer(f, lineterminator='\n', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow([*data])

    @staticmethod
    def record_logs(status_code: int, company_id: int=None, url: str=None) -> None:
        logging.basicConfig(filename='logs.log',
                    filemode='a',
                    format='%(asctime)s %(message)s', 
                    datefmt='%d.%m.%Y %H:%M:%S',
                    level=logging.INFO,
                    encoding='utf-8'
                    )

        if status_code != 200:
            logging.info(f'Status code: {status_code}')
            logging.info(f'Company with id {company_id} not found') if company_id else None
            logging.info(url) if url else None
