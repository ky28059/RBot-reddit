import praw
import config
import time
import os


def bot_login():
    print("Logging in...")
    bot = praw.Reddit(username=config.username,
                      password=config.password,
                      client_id=config.client_id,
                      client_secret=config.client_secret,
                      user_agent="The Reddit Commenter v1.0")
    print("Logged in!")

    return bot


def run_bot(bot, replied):
    replied = list(replied)
    print("Searching last 1,000 comments")

    for comment in bot.subreddit('Bot_testing_facility').comments(limit=1000):
        if "I love you RBot!" in comment.body and comment.id not in replied and comment.author != bot.user.me():
            print("String with \"sample user comment\" found in comment " + comment.id)
            comment.reply("Hey, I love you too!")
            print("Replied to comment " + comment.id)

            replied.append(comment.id)

            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")

    print("Search Completed.")

    print(replied)

    print("Sleeping for 10 seconds...")
    # Sleep for 10 seconds...
    time.sleep(10)


def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        replied = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            replied = f.read()
            replied = replied.split("\n")
            replied = filter(None, replied)

    return replied


r = bot_login()
comments_replied_to = get_saved_comments()
print(comments_replied_to)

while True:
    run_bot(r, comments_replied_to)
