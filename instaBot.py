from instapy import InstaPy

session = InstaPy(username = "username", password = "password") # Enter your instagram username and password
session.login()

while True:
    try:
        session.set_relationship_bounds(enabled = True, max_followers = 200)
        session.set_do_follow(True, percentage =100)
        session.set_do_comment(enabled=True, percentage=50) # optional
        session.like_by_tags(['tag1', 'tag2', 'tag3'], amount = 1) # Enter key words
        session.set_comments(['comment1', 'comment2', 'comment3']) # Set possible comments
    except Exception as e:
        print(e)
        pass

# find out how to use this module more on https://instapy.org/settings/
