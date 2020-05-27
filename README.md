# MarketWatch-Web-Crawler

Use Scrapy and Splash to parse articles from [MarketWatch](https://www.marketwatch.com/latest-news).

> MarketWatch is a website that provides financial information, business news, analysis, and stock market data. Along with The Wall Street Journal and Barron's, it is a subsidiary of Dow Jones & Company, a property of News Corp.

## Highlights
- Allow login to crawl full articles
- Load full pages with Splash
- Parse articles with Scrapy

## Using

### Setting Up Environment

First, install Splash. See [here](https://splash.readthedocs.io/en/stable/install.html#installation) for how to.Then go to you virtual environment install other packages by running
```console
pip install -r requirements.txt
```

### Launch Splash and Set up the ocal address in `settings.py`

Run code below in you shell(Linux) to run Splash locally. Make sure you set max-timeout to at least 100, or you will get `504 Time-Out` error .For other system, please refer [Splash HTTP API](https://splash.readthedocs.io/en/stable/api.html#splash-http-api).
```console
sudo docker run -it -p 8050:8050 scrapinghub/splash --max-timeout 3600
```

Replace `SPLASH_URL` with your local Splash address in `marketwatch/settings.py`.

### Set Dow Jones Account
If you want to log in to parse the full articles, please replace username and password in `marketwatch/settings.py` with your own,
```python
DOWJONES_USERNAME = 'your username'
DOWJONES_PASSWORD = 'your passcode'
```
and delete
```python
exec(open("../secret_settings").read())
```

If you don't want to log in, please delete the line above in `marketwatch/settings.py` and leave `DOWJONES_USERNAME` and `DOWJONES_PASSWORD` undefined. The code will catch up from there.

### Finally Run the crawler
cd to the project folder and run
```console
scrapy crawl latest -o <output_file_name.json>
```
You could also save it as `.csv` or `.xml`.

## Result
The output includes all avaialbe latest articles on marketwatch.com. They are sourced from wsj.com, Barron's and Marketwatch. See a sample full output in `latest.jason`.

### Example output for a flash headline
```json
{
    "frontpage_summary": {
        "label": "flash headline",
        "headline": "Boris Johnson and key adviser Cummings set to speak from Downing Street garden",
        "article_summary": null,
        "timestamp": "2020-05-25T11:06:04"
    }
},...
```
### Example output for a full article
```json
{
    "frontpage_summary": {
        "url": "https://www.marketwatch.com/story/lufthansa-secures-9-billion-stabilization-package-from-german-government-2020-05-25?mod=newsviewer_click",
        "headline": "Lufthansa secures €9 billion ‘stabilization package’ from German government",
        "article_summary": "German airline said it has received approval for a multibillion-dollar “stabilization package” from a government support fund to keep the company going through the turbulence from the coronavirus outbreak, but cautions the...",
        "label": ""
    },
    "category": [
        "Industries",
        "Airlines",
        "Associated Press"
    ],
    "header": {
        "headline": "Lufthansa secures €9 billion ‘stabilization package’ from German government",
        "sub_headline": "",
        "time_publish": "Published: May 25, 2020 at 12:41 p.m. ET",
        "time_update": ""
    },
    "author": {
        "author_name": "Associated Press",
        "author_link": "https://www.marketwatch.com/column/associated-press?mod=MW_author_byline"
    },
    "referenced_tickers": {
        "LHA": "+7.48%"
    },
    "paragraphs": [
        "FRANKFURT, Germany (AP) — German airline Lufthansa said Monday it has received approval for a €9 billion ($9.8 billion) “stabilization package” from a government support fund to keep the company going through the turbulence from the coronavirus outbreak, but cautions the deal has not been approved by the European Union’s executive commission.",
        "Lufthansa LHA, +7.48%, which has lost most of its passenger business due to travel restrictions during the outbreak, said the government’s fund has agreed to take non-voting holdings in return for 5.7 billion euros, plus a 3 billion-euro credit line and 300 million euros in share purchases.",
        "That would leave the government fund with a 20% stake in the company and two seats on the board of directors. One of those seats would be on the audit committee. The airline said however that the government agreed not to vote at shareholder meetings unless there was a takeover of the company.",
        "The government’s stake is below the level needed to block major decisions, but it has the option to raise it to a blocking stake of 25% plus one share in case of an attempted takeover of the company.",
        "The company’s trading statement said that the deal has not been approved by the European Commission, which could set conditions intended to preserve fair competition. The aid package would also require approval by a shareholder meeting.",
        "German business publication Handelsblatt said that German Chancellor Angela Merkel was resisting a push by the commission to make Lufthansa give up prized landing slots at its Frankfurt and Munich hubs."
    ],
    "related_articles": [
        "/investing/stock/LHA?countryCode=XE&mod=MW_story_quote"
    ]
},...
```
