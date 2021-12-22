from trending_videos import *

def test_is_same_list_size():
    assert len(video_link_list) == len(video_title_list) == len(video_channel_name_list) == len(channel_link_list) == len(video_views_list) == len(video_uploaded_list) == len(video_like_times_list) == len(subscribers_count_list)