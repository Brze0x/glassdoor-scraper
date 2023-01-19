# Glassdoor Scraper
This project is a parser that collects overviews and reviews of companies on glassdoor and saves them in CSV.

## Getting Started
To get reviews you need to specify the link and page number from which reviews will be collected.
![ui review](https://i.imgur.com/J0sHsdP.png)

To get an overview you need to specify the ID of the company whose data you want to collect.
![ui overview](https://i.imgur.com/Z6mA5VY.png)
You can see the ID in the link for example:
https://www.glassdoor.com/Overview/Working-at-Emazon-EI_IE6036.11,17.htm in this case the ID is 6036

The data is saved in CSV format to the "output" directory, which is located in "glassdoor-scraper\src\glassdoor_scraper\"

### Requirements
What things you need to use this scraper.
- Python v3.9 or above
- Beautiful Soup
- PySide6
- Requests

### Installation
A step by step series of examples that tell you how to get it running.
1. Clone the repository
`git clone https://github.com/Brze0x/glassdoor-scraper.git`
2. Go to project directory "glassdoor-scraper" and create and activate a virtual environment
`python.exe -m venv venv` and `.\venv\Scripts\activate`
3. Install dependencies using the requirements.txt
`pip install -r requirements.txt`

### Running
To start the scraper go to `glassdoor-scraper\src\glassdoor_scraper\` and run `python.exe .\main.py`
