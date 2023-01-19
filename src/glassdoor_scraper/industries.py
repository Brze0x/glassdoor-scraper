import re
import json
from common import Common


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
