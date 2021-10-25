from bs4 import BeautifulSoup
import requests
import time


class CrawlerError(Exception):
    pass


class Zakonkz:
    headers = {
        'authority': 'www.zakon.kz',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.zakon.kz/',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    def __init__(self, main_url):
        self.main_url = main_url

    def make_request(self, url, retries=3):
        attempts = 0
        while attempts < retries:
            retries += 1
            try:
                response = requests.get(url=url, headers=self.headers, timeout=10)
                print(url)

                # print(response.text)
                if response.ok:
                    return response.text
                else:
                    return None
            except requests.exceptions.RequestException as message:
                print(message)
                time.sleep(2)
                attempts += 1
            except AttributeError as message:
                print(message)
            except Exception:
                time.sleep(5)
                pass

    def get_proxy(self):
        url = "https://api.getproxylist.com/proxy?apiKey=f6c61e5fd4f84be48eecb62b8ceed766e7009340&maxConnectTime=1&minUptime=80&protocol=http&allowsHttps=1"

        response = requests.get(url)
        res = response.json()
        ip = res.get('ip')
        port = res.get('port')
        print(ip, port)

        proxy = {
            "http": f"http://{ip}:{port}",
            "https": f"http://{ip}:{port}"
        }
        return proxy

    def get_links(self, url, retries: int = 3):
        while retries > 0:
            retries -= 1
            html = self.make_request(url)

            soup = BeautifulSoup(html, "html.parser")
            links = []
            all_links = soup.find("div", class_="lastnews").find("ul")
            if all_links:
                li = all_links.find_all("li")
            else:
                continue

            for element in li:
                a = element.find("a")
                element_text = a.text
                element_url = a.get("href")
                element_url = self.main_url + element_url
                links.append(element_url)
            return links

    def get_soup(self, html):
        return BeautifulSoup(html, "html.parser")

    def parse_links(self, links: list):
        result = []
        if links:
            for link in links:
                html = self.make_request(link)
                soup = self.get_soup(html)
                title = self.get_title(soup)
                if title is not None:
                    description = self.get_description(soup)
                    publish_date = self.publish_date(soup)
                    # publish_date = #
                    res = {
                        'title': title,
                        'link': link,
                        'description': description,
                        'publish date': publish_date
                    }
                    # print(res)
                    result.append(res)
        return result

    @staticmethod
    def get_title(soup: BeautifulSoup):
        try:
            content = soup.find('div', class_="fullhead")
            title = content.find("h1").text
        except AttributeError:
            print("couldn't find a title:")
            return None

        return title

    @staticmethod
    def get_description(soup: BeautifulSoup):
        content = soup.find('div', class_="newscont")
        description = content.find_all("p")
        p_list = []
        for p in description:
            short_description = p.text
            p_list.append(short_description)
        result = ''.join(p_list)
        return result

    @staticmethod
    def publish_date(soup: BeautifulSoup):
        content = soup.find('div', class_="newsdate")
        publish_date = content.find('span').text
        return publish_date

    def loop(self):
        links = self.get_links(self.main_url)
        return self.parse_links(links)


if __name__ == "__main__":
    Zakonkz("https://www.zakon.kz/").loop()
