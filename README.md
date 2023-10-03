<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<br />
<p align="center">

  <h3 align="center">github-crawler</h3>

  <p align="center">
    Friendly github crawler. 
    </p>
</p>

# Setup
1. Install requirements
```
pip install -r requirement.txt
```
2. Update source url as per your need in `github/github/spiders/github-user.py`
```
def start_requests(self):
		urls = [
			"your search url here"
		]

```
## For CSV (default)
Set folllowing variables in `settings.py`
```    
ITEM_PIPELINES = {
   'GithubCsvPipeline': 300,
}
```

## For Elasticsearch
Set folllowing variables in `settings.py`
```    
ELASTICSEARCH_HOST = ''
ELASTICSEARCH_PORT = 9200
ITEM_PIPELINES = {
   'GithubElasticsearchPipeline': 300,
}

```
Note: This option requires index to be already created in the elasticsearch server 

## For Google sheet:
1. Set folllowing variables in `settings.py`
```
GOOGLE_SHEET =""
ITEM_PIPELINES = {
   'github.pipeline.GithubExcelPipeline': 300,
}
```
2. Store googleapi credentials in `utility/gsheets_credentials.json`

Note: This option requires an existing google sheet with permissions "Editable by anyone who has link"

# Run instructions
```
cd github
scrapy crawl github-user-search
```

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Ankush-Chander/github-crawler.svg?style=for-the-badge
[contributors-url]: https://github.com/Ankush-Chander/github-crawler/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Ankush-Chander/github-crawler.svg?style=for-the-badge
[forks-url]: https://github.com/Ankush-Chander/github-crawler/network/members
[stars-shield]: https://img.shields.io/github/stars/Ankush-Chander/github-crawler.svg?style=for-the-badge
[stars-url]: https://github.com/Ankush-Chander/github-crawler/stargazers
[issues-shield]: https://img.shields.io/github/issues/Ankush-Chander/github-crawler.svg?style=for-the-badge
[issues-url]: https://github.com/Ankush-Chander/github-crawler/issues
[license-shield]: https://img.shields.io/github/license/Ankush-Chander/github-crawler.svg?style=for-the-badge
[license-url]: https://github.com/Ankush-Chander/github-crawler/blob/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/ankush-chander-8248a876/
