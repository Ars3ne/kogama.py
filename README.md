# Kogama.py

[![Python Version](https://img.shields.io/badge/python-%E2%89%A53.5.3-yellow.svg)](https://www.python.org/downloads/)  [![Pypi](https://img.shields.io/pypi/v/kogama.py)](https://pypi.python.org/pypi/kogama.py/)

------

Copyright © 2019 Ars3ne

Licensed under the MIT License (see ``LICENSE.txt`` for details).

`Kogama <https://www.kogama.com>` is an online game where you can create, share and play multiplayer games created by other users.

Some features has been removed from the public version, in order to prevent abuse. If you need one of them, get in touch on Discord: ``Ars3ne#0497``

------


# Installation:
To install the library, just run the following command:
```
pip install kogama.py
```

### Requirements:

* Python ≥ 3.5.3
* ``requests``
* ``beautifulsoup4``

Usually ``pip`` will install these for you.

### Example
------
Here's a quick example of the library used to make a simple bot that get comments from a post and prints the content and id of them:

```python
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
```
------
### Documentation
Coming soon.
  
  
