import hashlib
import re
import traceback

import scrapy


class GithubUserSearchSpider(scrapy.Spider):
    """
    crawl user info from a search url
    """
    name = 'github-user-search'

    def start_requests(self):
        urls = [
            "https://github.com/search?l=Python&o=desc&q=location%3AIndia+followers%3A%3E5+repos%3A%3E3+language%3APython+location%3AIndia+followers%3A%3E5+repos%3A%3E2+language%3APython&s=followers&type=Users"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    @staticmethod
    def generate_unique_id_from_title(title):
        """
        Responsibility: Generate a unique id from input string.
        """
        regex = re.compile('[^a-zA-Z0-9]')
        m = hashlib.md5()
        title = title.lower()
        title = regex.sub('', title)
        m.update(title.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def _is_search_result_page(href):
        if "https://github.com/search?" in href and "&type=Users" in href:
            return True
        return False

    @staticmethod
    def _is_user_page(url):
        """
        Responsibility: Check if url is a user page.
        """
        return url.startswith("https://github.com") and url.count("?") == 0 and url.count("/") == 3 and url.split("/")[3] not in (
            "about", "collections", "customer-stories", "enterprise", "explore", "events", "features", "git-guides",
            "login", "marketplace", "mobile", "open-source", "pricing", "readme", "security", "signup", "site-map",
            "sponsors", "team", "topics", "trending", ""
        )

    @staticmethod
    def _ignore_page(url):
        """
        Responsibility: Check if url is to be ignored.
        """
        url_comps = url.split("/")
        try:
            if len(url_comps) > 3 and url_comps[4] in (
                    "", "about",
                    "collections", "customer-stories", "enterprise", "explore", "events", "features",
                    "git-guides", "login", "marketplace",
                    "mobile", "open-source", "pricing", "readme", "security", "signup", "site-map", "sponsors", "team",
                    "topics",
                    "trending") or "https://github.com" not in url:
                return True
        except Exception as err:
            print(traceback.format_exc())
            print(url)

        return False

    def parse_user_page(self, response):
        # extract date from page"s metadata
        try:
            fullname = response.xpath('//*[@class="p-name vcard-fullname d-block overflow-hidden"]/text()').get()
            if not fullname:
                return
            fullname = fullname.strip()

            username = response.xpath('//*[@class="p-nickname vcard-username d-block"]/text()').get()
            username = username.strip()
            github_link = f"https://github.com/{username}"

            try:
                followers, following, *_ = response.xpath(
                    '//*[@class="Link--secondary no-underline no-wrap"]/span/text()').getall()
                # print(f"res:{res}")
                # print(f"followers: {followers}, following: {following}, _: {_}")
            except Exception as err:
                raise Exception("follow count issue.")

            try:
                location = response.xpath(
                    "//li[contains(concat(' ',normalize-space(@class),' '),' vcard-detail ')]/span/text()").get()
            except Exception as err:
                location = ""

            try:
                links = response.xpath("//ul[@class='vcard-details']/li/a/@href").getall()
                twitter_link = [link for link in links if "twitter.com" in link]
                if twitter_link:
                    twitter_link = twitter_link[0]
                else:
                    twitter_link = ""
                other_links = [link for link in links if "twitter.com" not in link]
            except Exception as err:
                twitter_link = ""
                other_links = []

            try:
                description = response.xpath("//div[@class='Box-body p-4']//text()").getall()
                description = [item.strip() for item in description if item.strip()]
                description = " ".join(description)
            except Exception as err:
                print("description error")
                print(traceback.format_exc())
                pass

            try:
                last_year_activity = response.xpath("//div[@class='js-yearly-contributions']//h2/text()").get()
                last_year_activity = last_year_activity.replace("\n", "").strip()
            except Exception as err:
                last_year_activity = ""

            if fullname and username:
                doc_id = username
                item = {"doc_id": doc_id,
                        "username": username,
                        "fullname": fullname,
                        "description": description,
                        "followers": followers,
                        "following": following,
                        "github_link": github_link,
                        "twitter_link": twitter_link,
                        "location": location,
                        "other_links": other_links,
                        "last_year_activity": last_year_activity
                        }
                # print(item)
                yield item
        except Exception as err:
            print(traceback.format_exc())
            print(f"error while handling: {response.url}")
            pass

    def parse(self, response):
        # 2 alternatives: user page, search pagination page
        # print(f"parsing search page: {response.url}")
        # handle search page
        for link in response.css("a"):
            try:
                href = link.attrib.get('href', None)
                if not href:
                    continue

                if not href.startswith("https"):
                    href = response.urljoin(href)

                if self._is_user_page(href):
                    # crawl user page
                    yield scrapy.Request(href, callback=self.parse_user_page)
                elif self._is_search_result_page(href):
                    # crawl only next search result page
                    rel = link.attrib.get("rel", None)
                    if rel != "next":
                        continue
                    yield scrapy.Request(href, callback=self.parse)

            except Exception as err:
                print(traceback.format_exc())
