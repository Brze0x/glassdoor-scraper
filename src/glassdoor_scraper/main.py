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
            print(list(data.values()))

        # Common.save_to_json(job_titles, 'jobTitles')


if __name__ == "__main__":
    main()


# if os.path.exists('temp.json') and os.stat('temp.json').st_size > 0:
#     with open('temp.json', mode='r', encoding='utf-8') as f:
#         job_titles = json.load(f)
# else:
#     job_titles = {"JobTitlesByEmployer": []}

# x = Reviews()
# for page in range(1, 2):
#     print(f"Page number: {page}")
#     for data in x.get_job_titles(194, page):
#         job_titles["JobTitlesByEmployer"].append(data)

#     Common.save_to_json(job_titles, 'temp')

# x = Reviews()
# print(x.get_reviews(194, 1))




# ov = Overview()
# print(ov.get_overview(10212))
# employers = {"overview": [], "problemPages": []}

# for i in range(1, 10):
#     data = ov.get_overview(i)
#     if data:
#         employers["overview"].append(data)
#     else:
#         employers["problemPages"].append(i)

# Common.save_to_json(employers, 'temp')



# return {
#     "jobTitlesByEmployer": [
#         {
#             "id": json.loads(item)["id"], 
#             "jobTitle": json.loads(item)["text"]
#         } for item in re.findall(self.pattern, Common.get_script_tag_data(content[0]))
#     ]
# }



