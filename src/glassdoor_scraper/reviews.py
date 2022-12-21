import re
import json
from typing import Any
from common import Common


class Reviews:
    def __init__(self) -> None:
        self.pattern_job_title = r'\{"id":\d+,"__typename":"JobTitle","text":".*?"\}'
        self.pattern_review = r'\{"__typename":"EmployerReview",.*?,"translationMethod":.*?\}'

    @staticmethod
    def create_paginated_link(link: str, page_num: int) -> tuple[str, int]:
        company_id = link[link.index('E') + 1:link.index('.')]
        return link[:link.rindex('.')] + f"_P{page_num}" + link[link.rindex('.'):], company_id

    @staticmethod
    def get_employee_situation(review: dict) -> str:
        current = "Current" if review['isCurrentJob'] else "Former"
        status = review['employmentStatus']
        if status == "REGULAR":
            return f"{current} Employee"
        if status == "INTERN":
            return f"{current} Intern"
        if status == "CONTRACT":
            return f"{current} Contractor"
        if status == "PART_TIME":
            return f"{current} Employee - Part-time"
        if status == "FREELANCE":
            return f"{current} Freelancer"

    @staticmethod
    def get_job_title_by_id(jobs: list, job_id: int) -> str:
        for job in jobs:
            if job['id'] == job_id:
                return job['jobTitle']

    def validate_review(self, review: dict) -> dict:
        return {
                'title': review.get('summary'),
                'rating': review.get('ratingOverall'),
                'employeeSituation': self.get_employee_situation(review),
                'pros': review.get('pros'),
                'cons': review.get('cons'),
                'adviceToManagement': review.get('advice', 'No data')
            }

    def get_review_page_content(self, link: str, page_num: int, params: dict=None) -> tuple[str, int]:
        url = self.create_paginated_link(link, page_num)
        content = Common.get_page_content(url[0], params)
        Common.record_logs(content[-1], url[1], url[0])
        return content

    def get_job_titles(self, link: str, page_num: int) -> list[dict[str, Any]]:
        content = self.get_review_page_content(link, page_num)
        return [
            {
                "id": json.loads(item)["id"], 
                "jobTitle": json.loads(item)["text"]
            } for item in re.findall(self.pattern_job_title, Common.get_script_tag_data(content[0]))
        ]

    def get_raw_data(self, link: str, page_num: int, params: dict=None) -> list[dict[str, Any]]:
        content = self.get_review_page_content(link, page_num, params)
        return list(map(json.loads, re.findall(self.pattern_review, Common.get_script_tag_data(content[0]))))

    def get_reviews(self, link: str, page_num: int, params: dict=None) -> list[dict[str, Any]]:
        return list(map(self.validate_review, self.get_raw_data(link, page_num, params)))
