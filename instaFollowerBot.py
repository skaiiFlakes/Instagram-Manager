from instapy import InstaPy
import os

try:
    os.system("c:\\windows\\system32\\taskkill.exe /im firefox.exe /f")
except:
    print("firefox already closed")

session = InstaPy(username = "username", password = "password") # Enter your instagram username and password
session.login()

while True:
    try:
        session.set_relationship_bounds(enabled = True, max_followers = 200)
        session.like_by_tags(['tag1', 'tag2', 'tag3'], amount = 100) # Enter key word
        ssession.set_do_follow(True, percentage =50)
        session.set_dont_like(['tag1', 'tag2', 'tag3'])
        session.set_comments(['comment1', 'comment2', 'comment3']) # Set possible comments
        session.set_do_comment(enabled=True, percentage=50) # optional
        
    except Exception as e:
        print(e)
        pass

# find out more uses of this module on https://instapy.org/settings/
