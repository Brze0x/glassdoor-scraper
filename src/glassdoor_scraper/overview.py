import re
import json
from typing import Any
from typing import Union
from common import Common


class Overview:
    def __init__(self) -> None:
        self.pattern = r"(\"Employer:\d+\":)(.+)(,\"ROOT_QUERY\")"
        # self.employers = {"overview": [], "problemPages": []}

    @staticmethod
    def get_url(company_id: int) -> str:
        return f"https://www.glassdoor.com/Overview/Working-at-EI_IE{company_id}.htm"

    def check_item(self, data: Union[dict, None], key: str) -> Union[str, None]:
        if data:
            return data.get(key)

    def validate_data(self, data: str) -> str:
        if data:
            data = re.sub(r'\n', " ", data)
            data = re.sub(r'\r', " ", data)
            data = re.sub(r',', r'\,', data)
            data = re.sub(r' +', ' ', data)
            return data

    def validate_json(self, data: dict) -> dict[str, Any]:
        return {
            "id": data["id"],
            "shortName": data["shortName"],
            "reviewsUrl": data["links"]["reviewsUrl"],
            "website": data["website"],
            "type": data["type"],
            "revenue": data["revenue"],
            "headquarters": data["headquarters"],
            "size": data["size"],
            "stock": data["stock"],
            "yearFounded": data["yearFounded"],
            "industryName": self.check_item(data["primaryIndustry"], "industryName"),
            "description": self.validate_data(data["overview"]["description"]),
            "mission": self.validate_data(data["overview"]["mission"])
        }

    def get_overview(self, company_id: int) -> Union[dict[str, Any], None]:
        url = self.get_url(company_id)
        content = Common.get_page_content(url)
        Common.record_logs(content[-1], company_id, url)
        try:
            data = json.loads(re.findall(self.pattern, Common.get_script_tag_data(content[0]))[0][1])
        except IndexError:
            return None
        return self.validate_json(data)
