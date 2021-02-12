# find out more uses of this module on https://instapy.org/settings/
from instapy import InstaPy
import os
import time

#Enter instagram account details
username = ""
password = ""

def start():
    try:
        os.system("c:\\windows\\system32\\taskkill.exe /im firefox.exe /f") #Ensure that the path to taskkill.exe is correct
    except:
        print("firefox already closed")

def follow_by_tags():
    session = InstaPy(username = username, password = password, headless_browser=True)
    session.login()
    session.set_relationship_bounds(enabled = True, max_followers = 200)
    while True:
        try:
            session.set_do_follow(True, percentage = 100)
            session.set_comments([]) #Enter a list of comments
            session.set_do_comment(enabled=True, percentage=60)
            session.set_dont_like([]) #Enter a list of tags you don't want to include
            session.like_by_tags([], amount = 6) #Enter a list of tags you want to include
        except:
            pass

def follow_fof():
    session = InstaPy(username = username, password = password, headless_browser=True)
    session.login()
    while True:
        try:
            accounts = [] # Enter a list of chosen followers
            session.follow_user_followers(accounts, amount=20, randomize = False)
        except:
            pass

def unfollow():
    session = InstaPy(username = username, password = password, headless_browser=True)
    session.login()
    while True:
        try:
            session.unfollow_users(amount="full", instapy_followed_enabled=True, instapy_followed_param="nonfollowers", style="FIFO", unfollow_after=90*60*60, sleep_delay=501)
        except:
            pass

while userinput != 0 and userinput != 1 and userinput != 2:
    userinput = int(input("\n0: Follow by tags\n1: Follow Followers' Followers\n2: Unfollow Nonfollowers Followed by InstaPy\n\nEnter: "))
if userinput == 0:
    start()
    follow_by_tags()
elif userinput == 1:
    start()
    follow_fof()
elif userinput == 2:
    start()
    unfollow()
