def test_reset_views():
    views = ""
    views2 = "觀看次數：290萬次"
    views3 = "2 天前"
    views4 = "直播時間：17 小時前"
    assert reset_views(views) == None
    assert reset_views(views2) == '290萬次'
    assert reset_views(views3) == None
    assert reset_views(views4) == None


def reset_views(views):
    if "觀看次數" in views:
        return views[views.find("：")+1:]
    else:
        return None


def test_reset_upload():
    views = ""
    views2 = "觀看次數：290萬次"
    upload = "2 天前"
    assert reset_upload(views) != ""
    assert reset_upload(views2) != '觀看次數：290萬次'
    assert reset_upload(upload) == "2 天前"


def reset_upload(upload):
    if " " in upload:
        return upload


def replace_comma(string):
    return int(string.replace(",", ""))


def test_replace_comma():
    string = "645,017"
    assert replace_comma(string) == 645017
