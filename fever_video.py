import time
import json
import locale
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as Soup

from test_case import reset_views, reset_upload,replace_comma


all_fever_viedo = []
fever_video_data = {"link": "", "video title": "", "channel name": "", "channel link": "",  "views": 0, "uploaded": "", "likes times": "", "subscribers": "", "comments": ""}

video_link_list = []
video_title_list = []
video_channel_name_list = []
video_channel_link_list = []
video_views_list = []
video_post_time_list = []
video_like_times_list = []
subscribers_list = []

with webdriver.Chrome() as driver:
    yt_fever_url = "https://www.youtube.com/feed/trending?bp=6gQJRkVleHBsb3Jl"
    driver.get(yt_fever_url)

    # for item in range(95):
    driver.execute_script("window.scrollTo(0, 99999)")
    time.sleep(2)

    for title in driver.find_elements(By.CLASS_NAME, 'yt-simple-endpoint.style-scope.ytd-video-renderer'):
        video_title_list.append(title.get_attribute('title'))
        video_link_list.append(title.get_attribute('href'))

    search_channel_name = driver.find_elements(By.CLASS_NAME, 'yt-simple-endpoint.style-scope.yt-formatted-string')
    for channel_name in search_channel_name:
        if channel_name not in search_channel_name[5:9]:
            print(channel_name.text)
            if len(channel_name.text) != 0:
                video_channel_name_list.append(channel_name.text)
                video_channel_link_list.append(channel_name.get_attribute('href'))


c = 0
with webdriver.Chrome() as video:
    for fever_video_url in video_link_list[:]:
        try:
            print(c)
            c+=1
            video.get(fever_video_url)
            video.execute_script("window.scrollTo(0, 99999)")
            time.sleep(7)
            temp = video.find_elements(By.TAG_NAME, 'yt-formatted-string')

            views = video.find_element(By.CLASS_NAME, 'view-count.style-scope.ytd-video-view-count-renderer').text
            video_views_list.append(replace_comma(views[views.find("：")+1: -1]))
            for upload in temp[9:10]:
                video_post_time_list.append(upload.text)

            temp = video.find_elements(By.ID, 'text')
            for like_times in temp[2:3]:
                video_like_times_list.append(like_times.text)

            subscribers = video.find_element(By.ID, 'owner-sub-count')
            subscribers_list.append(subscribers.text[:subscribers.text.find(" ")])
        except:
            c += 1
            video_views_list.append(None)
            video_post_time_list.append(None)
            video_like_times_list.append(None)
            subscribers_list.append(None)


print(video_post_time_list)
print(video_like_times_list)
print(subscribers_list)

for times in range(len(video_title_list)):
    fever_video_data["video title"] = video_title_list[times]
    fever_video_data["link"] = video_link_list[times]
    fever_video_data["views"] = video_views_list[times]
    fever_video_data["channel name"] = video_channel_name_list[times]
    fever_video_data["channel link"] = video_channel_link_list[times]
    fever_video_data["uploaded"] = video_post_time_list[times]
    fever_video_data["likes times"] = video_like_times_list[times]
    fever_video_data["subscribers"] = subscribers_list[times]
    all_fever_viedo.append(fever_video_data.copy())


filename = "youtube fever video.json"
with open(filename, 'w') as w_f:
    yt_fever_video_data = all_fever_viedo
    w_f.write(json.dumps(yt_fever_video_data, sort_keys=True, indent=4))

    print(yt_fever_video_data)
