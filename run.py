from flask import Flask, request, jsonify, json
from twython import Twython

app = Flask(__name__)

class AccountInfo() :
    # "fullname": "Raymond Hettinger",
    # "href": "/raymondh",
    # "id": 14159138

    def __init__(self, accInfo) :
        self.fullname = accInfo["name"]
        self.href = "/" + accInfo["screen_name"]
        self.id = accInfo["id"]

    def toJson(self):
        return json.dumps(self.__dict__)

class StatusInfo() :
    # "date": "12:57 PM - 7 Mar 2018",
    # "hashtags": ["#python"],
    # "likes": 169,
    # "replies": 13,
    # "retweets": 27,
    # "text"
    def __init__(self, account, date, hashtags, likes, replies, retweets, text):
        self.account = account
        self.date = date
        self.hashtags= hashtags
        self.likes = likes
        # self.replies = replies
        self.retweets = retweets
        self.text = text

    def toJson(self):
        return json.dumps(self.__dict__)



@app.route("/")
def hello():
    return "Hello World!"

@app.route("/hashtags/<string:tags>")
def getbyhashtags(tags):
    print("hash tags is : " + '#' + tags)
    page_limit = request.args.get('page_limit')
    TWITTER_ACCESS_TOKEN = '1011888759900553216-Z4wzLrjRFSDER0LfGWSn8mPFta8aAe'
    TWITTER_ACCESS_TOKEN_SECRET = 'vrlmK45hMritNtPYQ2VA9MgaAuhcIMNjO9nTPL1Je2xiF'
    TWITTER_APP_KEY = 'uOEdyXkcbLynEl7Rni18Mz8ta'
    TWITTER_APP_KEY_SECRET = 'ALKBu4uFOxZLoLmrv2FVUfx90T5UO1yFDi7lUMJ0PC22qv9Zl8'
    twitter = Twython(
        TWITTER_APP_KEY,
        TWITTER_APP_KEY_SECRET,
        TWITTER_ACCESS_TOKEN,
        TWITTER_ACCESS_TOKEN_SECRET
    )
    search_results = twitter.search(q='#' + tags, count = page_limit)
    print(search_results["statuses"])
    list_data = []
    for element in search_results["statuses"]:
        account = AccountInfo(element["user"])
        hashTags = []
        for tag in element["entities"]["hashtags"] :
            hashTags.append("#" + tag["text"])
        status = StatusInfo(
            account.toJson(),
            element["created_at"],
            hashTags,
            element["favorite_count"],
            '',
            element["retweet_count"],
            element["text"]
        )
        list_data.append(status.toJson())
    return jsonify(list_data)

if __name__ == "__main__":
    app.run()
