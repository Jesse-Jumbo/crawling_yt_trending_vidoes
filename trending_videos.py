import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from test_case import replace_comma
all_trending_video = []
trending_video_data = {"video_link": "", "video_title": "", "channel_name": "", "channel_link": "",  "views": 0, "uploaded": "", "likes_times": "", "subscribers_count": ""}

video_link_list = []
video_title_list = []
video_channel_name_list = []
channel_link_list = []
video_views_list = []
video_uploaded_list = []
video_like_times_list = []
subscribers_count_list = []

def main():
    with webdriver.Chrome() as driver:
        yt_trending_url = "https://www.youtube.com/feed/trending?bp=6gQJRkVleHBsb3Jl"
        driver.get(yt_trending_url)

        driver.execute_script("window.scrollTo(0, 99999)")
        time.sleep(2)

        for title in driver.find_elements(By.CLASS_NAME, 'yt-simple-endpoint.style-scope.ytd-video-renderer'):
            video_title_list.append(title.get_attribute('title'))
            video_link_list.append(title.get_attribute('href'))

        search_channel_name = driver.find_elements(By.CLASS_NAME, 'yt-simple-endpoint.style-scope.yt-formatted-string')
        for channel_name in search_channel_name:
            print(channel_name.text)
            if len(channel_name.text) != 0:
                video_channel_name_list.append(channel_name.text)
                channel_link_list.append(channel_name.get_attribute('href'))

    with webdriver.Chrome() as driver:
        c = 0
        for trending_video_url in video_link_list[:]:
            try:
                c += 1
                driver.get(trending_video_url)
                driver.execute_script("window.scrollTo(0, 99999)")
                time.sleep(7)

                views = driver.find_element(By.CLASS_NAME, 'view-count.style-scope.ytd-video-view-count-renderer').text
                video_views_list.append(replace_comma(views[views.find("：")+1: -1]))

                temp = driver.find_elements(By.TAG_NAME, 'yt-formatted-string')
                for upload in temp[9:10]:
                    video_uploaded_list.append(upload.text)

                temp = driver.find_elements(By.ID, 'text')
                for like_times in temp[2:3]:
                    video_like_times_list.append(like_times.text)
                    print(video_like_times_list)
                subscribers = driver.find_element(By.ID, 'owner-sub-count').text
                subscribers_count_list.append(subscribers[:subscribers.find(" ")])
            except Exception as e:
                print(c, e)
                c += 1
                video_views_list.append(None)
                video_uploaded_list.append(None)
                video_like_times_list.append(None)
                subscribers_count_list.append(None)

    for times in range(len(video_link_list)):
        trending_video_data["video_title"] = video_title_list[times]
        trending_video_data["video_link"] = video_link_list[times]
        trending_video_data["views"] = video_views_list[times]
        trending_video_data["channel_name"] = video_channel_name_list[times]
        trending_video_data["channel_link"] = channel_link_list[times]
        trending_video_data["uploaded"] = video_uploaded_list[times]
        trending_video_data["likes_times"] = video_like_times_list[times]
        trending_video_data["subscribers_count"] = subscribers_count_list[times]
        all_trending_video.append(trending_video_data.copy())

    save_to_json('trending_video_data.json', all_trending_video)


def save_to_json(self, filename: str, data):
    with open(filename, 'w') as json_file:
        save_data = data
        json_file.write(json.dumps(save_data, sort_keys=True, indent=4))
    return json_file


if __name__ == "__main__":
    main()
