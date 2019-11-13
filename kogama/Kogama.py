''''
/*
 * Kogama.py - Version 0.1.4
 * Developed by: Ars3ne
*/
'''

from .Exceptions import InvalidServerException, BannedUserException, UnauthorizedException
from bs4 import BeautifulSoup
import requests
import json
import re

class Kogama(object):
    """ A class that represents a KoGaMa user.
        The 'server paramter can be set to one of 'www', 'br', or 'friends' (case insensitive).
    """
    def __init__(self, server):

        servers = {
          "www": "https://www-lb1.kgoma.com",
          "br": "https://br-lb3.kgoma.com",
          "friends": "https://friends-lb1.kgoma.com",
        }

        try:
          self.server = servers[server.lower()]
        except KeyError:
          raise InvalidServerException("The server provided is invalid.")

        self.session = requests.Session()

        self.headers = {}
        self.headers['User-agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        self.headers['Content-type'] = "application/json"
        self.headers['X-Requested-With'] = "XMLHttpRequest"

        self.csrf_token = ""
        self.userId = 0

    class _Auth(object):
      def __init__(self, kogama):
        self.kogama = kogama
        self.server = self.kogama.server
        self.session = self.kogama.session
        self.userId = self.kogama.userId
        self.headers = self.kogama.headers

      def login(self, username, password):
        """ Try to login the user in KoGaMa using the specified username and password.
            Returns True if the user is signed in, returns False if an error occoured during the login.
            Raises BannedUserException if the user is banned.
        """
        data = {
          "csrf_token": "",
          "username": "" + username + "",
          "password": "" + password + ""
        }

        r = self.session.post('{}/auth/login/'.format(self.server), json=data, headers=self.headers)

        j = json.loads(r.text)

        if 'error' not in j:

            self.kogama.userId = j['data']['id']
            r = self.kogama.session.get('{}'.format(self.server))
            soup = BeautifulSoup(r.text, 'lxml')
            self.kogama.csrf_token = soup.select_one('meta[name="CSRFToken"]')['content']

            self.kogama.headers = {}
            self.kogama.headers['User-agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
            self.kogama.headers['Content-type'] = "application/json"
            self.kogama.headers['X-Requested-With'] = "XMLHttpRequest"
            self.kogama.headers['X-Csrf-Token'] = self.kogama.csrf_token

            return True
        else:
          if 'banido' in r.text or 'banned' in r.text:
            raise BannedUserException('This user is banned.')
          else:
            return False

      def register(self, username, password, avatar=25):
        """ Try to register a account on KoGaMa.
            Returns True if the user was registred. Returns False if an error occoured.
            In order to prevent abuse, this function has been removed from the public version.
        """
        return False

      def logout(self):
        """ Logout user from KoGaMa. Returns True."""
        self.session.get("{}/auth/logout".format(self.server))
        self.session.cookies.clear()
        return True

    class _User(object):

      def __init__(self, kogama):
        self.kogama = kogama
        self.server = self.kogama.server
        self.session = self.kogama.session
        self.userId = self.kogama.userId
        self.headers = self.kogama.headers

      def add_post(self, profileId, content):
        """In order to prevent abuse, this function has been removed from the public version."""
        return False

      def add_comment(self, postId, content):
        """In order to prevent abuse, this function has been removed from the public version."""
        return False

      def get_post_comments(self, postId):
        r = self.session.get('{}/api/feed/{}/comment/'.format(self.server, postId), headers=self.headers)
        return json.loads(r.text)

      def add_friend(self, friendId):
        """In order to prevent abuse, this function has been removed from the public version."""
        return False

      def remove_friend(self, friendId):
        self.session.delete('{}/user/{}/friend/{}'.format(self.server, self.userId, friendId), headers=self.headers)
        return True

      def redeem_coupon(self, code):
        data = {
          "code": ""+code+""
        }

        r = self.session.post('{}/api/coupon/redeem'.format(self.server), json=data, headers=self.headers)
        j = json.loads(r.text)
        if "error" not in j:
          return j
        else:
          return False

      def change_description(self, description):
        """In order to prevent abuse, this function has been removed from the public version."""
        return False

      def change_username(self, username):
        """In order to prevent abuse, this function has been removed from the public version."""
        return False

      def claim_elite_gold(self):
        r = self.session.post('{}/user/{}/claim-daily-gold'.format(self.server, self.userId), headers=self.headers)

        if r.status_code == 200:
          return json.loads(r.text)
        else:
          return False

      def get_info(self):
        r = self.session.get('{}/user/{}'.format(self.server, self.userId), headers=self.headers)
        return json.loads(r.text)

    class _Game(object):
      def __init__(self, kogama):
        self.kogama = kogama
        self.server = self.kogama.server
        self.session = self.kogama.session
        self.userId = self.kogama.userId
        self.headers = self.kogama.headers

      def get_info(self, gameId):
        g = self.session.get("{}/games/play/{}".format(self.server, gameId))
        if g.status_code == 200:
          html = g.content
          soup = BeautifulSoup(html, 'lxml')
          data = soup.find_all("script")[10].string
          options = re.findall("options.bootstrap\\s*=(.+)", data)
          game_json = json.loads(options[0][:-1])
          return game_json['object']
        else:
          return False

      def get_comments(self, gameId):
        r = self.session.get('{}/game/{}/comment'.format(self.server, gameId), headers=self.headers)
        return json.loads(r.text)

      def add_comment(self, gameId, comment):
        """In order to prevent abuse, this function has been removed from the public version."""
        return False

      def remove_comment(self, gameId, commentId):
        r = self.session.delete('{}/game/{}/comment/{}'.format(self.server, gameId, commentId), headers=self.headers)
        j = json.loads(r.text)
        if  "error" not in j:
          return True
        else:
          if "Unauthorized" in j:
            raise(UnauthorizedException("You are not a member of the target game."))
          else:
            return False

      def like(self, gameId):
        """In order to prevent abuse, this function has been removed from the public version."""
        return False

      def invite(self, gameId, playerId):
        """In order to prevent abuse, this function has been removed from the public version."""
        return False

      def accept_invite(self, gameId):
        data = {
          "type": "pending",
          "status": "accept"
        }

        r = self.session.put('{}/game/{}/member/{}'.format(self.server, gameId, self.userId), json=data, headers=self.headers)
        j = json.loads(r.text)
        if j is None:
          return True
        else:
          return False

      def change_description(self, gameId, description):
        """In order to prevent abuse, this function has been removed from the public version."""
        return False

      def change_name(self, gameId, name):
        """In order to prevent abuse, this function has been removed from the public version."""
        return False

    class _Market(object):

      def __init__(self, kogama):
        self.kogama = kogama
        self.server = self.kogama.server
        self.session = self.kogama.session
        self.userId = self.kogama.userId
        self.headers = self.kogama.headers

      def get_info(self, itemId):
        r = self.session.get('{}/model/market/{}'.format(self.server, itemId), headers=self.headers)
        return json.loads(r.text)

      def buy(self, itemId):
        """In order to prevent abuse, this function has been removed from the public version."""
        return False

      def get_comments(self, itemId):
        r = self.session.get('{}/model/market/{}/comment'.format(self.server, itemId), headers=self.headers)
        return json.loads(r.text)

      def add_comment(self, itemId):
        """In order to prevent abuse, this function has been removed from the public version."""
        return False

      def remove_comment(self, itemId, commentId):
        r = self.session.delete('{}/model/market/{}/comment/{}'.format(self.server, itemId, commentId), headers=self.headers)
        j = json.loads(r.text)
        if "error" not in j:
          return True
        else:
          if "Unauthorized" in r.text:
            raise(UnauthorizedException("You are not the author of the comment."))
          else:
            return False

    def Auth(self):
      return self._Auth(self)

    def User(self):
      return self._User(self)

    def Game(self):
      return self._Game(self)

    def Market(self):
      return self._Market(self)
