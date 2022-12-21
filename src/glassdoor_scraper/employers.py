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


class Industries:
    def __init__(self) -> None:
        self.url = 'https://www.glassdoor.com/Reviews/index.htm'
        self.pattern = r"(\"industries\"):(.*\}\]),(\"sectors\")"
        self.industries = {"industries":[]}

    def get_industries(self) -> dict[str, list]:
        content = Common.get_page_content(self.url)
        data = json.loads(re.findall(self.pattern, Common.get_script_tag_data(content[0]))[0][1])
        for item in data:
            data = {
                "industryId": item["industryId"],
                "industryName": item["industryName"]
            }
            self.industries["industries"].append(data)
        return self.industries


# employers = Employers()
# emp = employers.get_employers_from_pages(1, 30)
# print(len(emp['employers']))
# if emp['problemPages']:
#     get_miss_data = employers.get_employers_from_problem_pages(emp['problemPages'])
#     print(len(get_miss_data['employers']))

# industries = Industries()
# print(industries.get_industries())



# industries = {"industries":[]}

# if os.path.exists('employers.json'):
#     with open('employers.json', mode='r', encoding='utf-8') as f:
#         employers = json.load(f)
# else:
#     employers = {"employers":[], "problemPages": []}


# get_employers_from_pages(employers, 1, 30)
# get_employers_from_problem_pages(employers['problemPages'])
# employers['employers'] = sort_list_of_dicts(employers['employers'], "id")
# save_to_json(employers, 'employers')



# pattern_industries = r"(\"industries\"):(.*\}\]),(\"sectors\")"
# pattern_employer = r"({\"id\":\d+,\"name\":.*?})\}\){1,}"

# with open(file='jobTitles.json', mode='r', encoding='utf-8') as f:
#     d = json.load(f)

# with open('t.json', mode='a', encoding='utf-8') as f:
#     for i in sorted([dict(t) for t in {tuple(d.items()) for d in d["JobTitlesByEmployer"]}], key=lambda x: x["jobTitleId"]):
#         json.dump(i, f, ensure_ascii=False, indent=4)


# with requests.Session() as session:
    # session.headers.update(headers)
    # response = session.get('https://www.glassdoor.com/Explore/browse-companies.htm?overall_rating_low=3&page=325')
    # raw_data = response.text
    # script = [s.text for s in BeautifulSoup(raw_data, "lxml").find_all("script") if "window.appCache" in s.text][0]
    # script = re.sub(r"\\{2,}\"", r"'", script)
    # script = re.sub(r"\\{1}", r"", script)

    # print(len(re.findall(pattern_employer, script)[::2]))
    # print(re.findall(pattern_employer, script)[::2])

    # with open('text.txt', 'w', encoding='utf-8') as f:
    #     f.write(script)    


    

    # json_data = json.loads(re.findall(pattern_employer_id, script)[0][1])
    # for item in json_data:
    #     data = {
    #         "industryId": item["industryId"],
    #         "industryName": item["industryName"]
    #     }
    #     industries["industries"].append(data)

    # with open('temp.json', mode='w', encoding='utf-8') as f:
    #     json.dump(employers, f, ensure_ascii=False, indent=4)


# pattern = r"(\"industries\"):(.*\}\]),(\"sectors\")"
# headers = {
#     'user-agent': 'Mozilla/5.0'
# }
# industries = {"industries":[]}

# with requests.Session() as session:
#     session.headers.update(headers)
#     response = session.get('https://www.glassdoor.com/Reviews/index.htm?overall_rating_low=3&page=1', timeout=60)
#     raw_data = response.text
#     script = [s.text for s in BeautifulSoup(raw_data, "lxml").find_all("script") if "window.appCache" in s.text][0]
#     json_data = json.loads(re.findall(pattern, script)[0][1])



    # for employer in employers_data:
    #     if employer not in employers["employers"]:
    #         employers["employers"].append(employer)