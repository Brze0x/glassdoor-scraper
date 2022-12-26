import os
import json
from common import Common
from reviews import Reviews
from overview import Overview


def main():
    url = 'https://www.glassdoor.com/Reviews/Target-Reviews-E194.htm'
    reviews = Reviews()

    if os.path.exists('jobTitles.json') and os.stat('jobTitles.json').st_size > 0:
        with open('jobTitles.json', mode='r', encoding='utf-8') as f:
            job_titles = json.load(f)
    else:
        job_titles = {"JobTitlesByEmployer": []}

    for page in range(1, 10):
        print(f"Page number: {page}")
        for data in reviews.get_job_titles(url, page):
            # job_titles["JobTitlesByEmployer"].append(data)
            Common.save_to_csv(list(data.values()), 'jobTitles')

        # Common.save_to_json(job_titles, 'jobTitles')


if __name__ == "__main__":
    main()
