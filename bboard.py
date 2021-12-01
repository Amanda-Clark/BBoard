import requests

from datetime import datetime as dt2
from flask import Flask
from flask import render_template

app = Flask(__name__)
app.config.from_object('config')
latitude = app.config["LATITUDE"]
longitude = app.config["LONGITUDE"]
news_key = app.config["NEWS_API_KEY"]
weather_key = app.config["WEATHER_API_KEY"]


def cur_cond(r):
    curTemp = str(r.json()['current']['temp'])
    desc = r.json()['current']['weather'][0]['description']
    windSpd = str(r.json()['current']['wind_speed'])
    windDegree = str(r.json()['current']['wind_deg'])
    visibility = r.json()['current']['visibility']
    visibility = visibility / 1000
    visibility = str(visibility)
    humidity = str(r.json()['current']['humidity'])
    time = r.json()['current']['dt']
    time = str(dt2.utcfromtimestamp(time).strftime('%Y-%m-%d %H'))
    sunrise = r.json()['current']['sunrise']
    sunrise = str(dt2.utcfromtimestamp(sunrise).strftime('%H:%M:%S'))
    sunset = r.json()['current']['sunset']
    sunset = str(dt2.utcfromtimestamp(sunset).strftime('%H:%M:%S'))
    feelslike = str(r.json()['current']['feels_like'])
    pressure = str(r.json()['current']['pressure'])
    dewpoint = str(r.json()['current']['dew_point'])
    clouds = str(r.json()['current']['clouds'])
    uvi = str(r.json()['current']['uvi'])
    return curTemp, desc, windSpd, windDegree, visibility, humidity, time, sunrise, sunset, feelslike, pressure, \
           dewpoint, clouds, uvi


class Alert(object):
    def __init__(self, *args):
        args = list(args)
        self.sender = args[0]
        self.event = args[1]
        self.start = args[2]
        self.end = args[3]
        self.description = args[4]


class Stories:
    def __init__(self, name, title, description, publishedat, content):
        self.name = name
        self.title = title
        self.description = description
        self.publishedat = publishedat
        self.content = content


def getnews(newsdata):
    stories = []
    for item in newsdata.json()['articles']:
        name = item['source']['name']
        title = item['title']
        description = item['description']
        publishedat = item['publishedAt']
        content = item['content']
        story = Stories(name, title, description, publishedat, content)
        stories.append(story)
    return stories


def cur_alert(r):
    sender = str(r[0]['sender_name'])
    event = str(r[0]['event'])
    start = r[0]['start']
    end = r[0]['end']
    description = str(r[0]['description'])
    return sender, event, start,  end, description


class CurrWthr(object):
    def __init__(self, *args):
        args = list(args)
        self.curTemp = args[0]
        self.desc = args[1]
        self.windSpd = args[2]
        self.windDegree = args[3]
        self.visibility = args[4]
        self.humidity = args[5]
        self.time = args[6]
        self.sunrise = args[7]
        self.sunset = args[8]
        self.feelslike = args[9]
        self.pressure = args[10]
        self.dewpoint = args[11]
        self.clouds = args[12]
        self.uvi = args[13]


@app.route('/')
def return_board():
    result = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=" + latitude + "&lon="
                          + longitude + "&units=imperial&exclude=minutely,hourly&appid=" + weather_key)

    newsdata = requests.get("https://newsapi.org/v2/top-headlines?country=us&pageSize=15&"
                            "apiKey="+news_key)
    othernews = requests.get("https://newsapi.org/v2/top-headlines?country=us&q=covid&pageSize=15&"
                             "apiKey="+news_key)
    storylist = getnews(newsdata)
    othernews = getnews(othernews)
    curTemp, desc, windSpd, windDegree, visibility, humidity, time, srise, sset, feels, press, dew, clds, uvi = \
        cur_cond(result)

    if 'alerts' in result.json():
        sender, event, start, end, description = cur_alert(result.json()['alerts'])

        alert = Alert(sender, event, start, end, description)
        alert.start = dt2.utcfromtimestamp(alert.start).strftime('%Y-%m-%d %H:%M:%S')
        alert.end = dt2.utcfromtimestamp(alert.end).strftime('%Y-%m-%d %H:%M:%S')
        current = CurrWthr(curTemp, desc, windSpd, windDegree, visibility, humidity, time, srise, sset, feels, press,
                       dew, clds, uvi)
        return render_template('board.html', data=current, alerts=alert, news=storylist, flag="alert",
                              ornews=othernews)
    else:
        current = CurrWthr(curTemp, desc, windSpd, windDegree, visibility, humidity, time, srise, sset, feels, press,
                           dew, clds, uvi)
        return render_template('board.html', data=current, flag="noalert", news=storylist, ornews=othernews)


if __name__ == '__main__':
    app.run()
