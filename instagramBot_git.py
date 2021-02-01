from instapy import InstaPy

session = InstaPy(username = "username", password = "password") # Enter your instagram username and password
session.login()

while True:
    try:
        session.set_relationship_bounds(enabled = True, max_followers = 200)
        session.set_do_follow(True, percentage =100)
        session.set_do_comment(enabled=True, percentage=50)
        session.like_by_tags(['tag1', 'tag2', 'tag3'], amount = 1) # Enter key words
        session.set_comments(['Awesome', 'Really Cool', 'I like your work!', 'Woah'])
    except Exception as e:
        print(e)
        pass

# https://instapy.org/settings/
# add to git repository