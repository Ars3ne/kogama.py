from kogama import Kogama
import json

k = Kogama.Kogama("www")
l = k.Auth().login("username", "password")

if l:
  comments = k.User().get_post_comments(20782273)
  for comment in comments['data']:
    comment_text = json.loads(comment['_data'])
    print("Comment: {}. ID: {}".format(comment_text['data'], comment['id']))
else:
  exit("Unable to login.")

exit()