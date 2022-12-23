from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
from urllib.request import urlopen

# downloads the video
def downloadVideo(link, id):
    cookies = {
        'ad_client': 'ssstik_back',
        '__cflb': '02DiuEcwseaiqqyPC5qr2kcTPpjPMVimtfdy3gS9TyoaK',
    }

    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'ad_client=ssstik_back; __cflb=02DiuEcwseaiqqyPC5qr2kcTPpjPMVimtfdy3gS9TyoaK',
        'hx-current-url': 'https://ssstik.io/en',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/en',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'YUpWQUc4',
    }

    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")
    downloadLink = downloadSoup.a["href"]
    mp4File = urlopen(downloadLink)
    with open(f"videos/{id}.mp4", "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break

# specifies that the web is Chrome and opens the url on Chrome
tiktok_user = input("Enter the url of the TikTok users' home page: ")
driver = webdriver.Chrome()
driver.get(tiktok_user)
time.sleep(1)

# scrolls down the tiktok page so that the driver can get all the videos
scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    # break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break 

# gets all the videos w bs4
soup = BeautifulSoup(driver.page_source, "html.parser")
videos = soup.find_all("div", {"class": "tiktok-yz6ijl-DivWrapper"})

#downloads all the videos in the users' tiktok profile
print(f"Number of videos: {len(videos)}")
for index, video in enumerate(videos):
    downloadVideo(video.a["href"], index)
    time.sleep(10)

