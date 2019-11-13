class InvalidServerException(Exception):
  """Raised when the user inputs a invalid server"""
  pass

class BannedUserException(Exception):
  """Raised when the user tries to login on a banned account"""
  pass

class UnauthorizedException(Exception):
  """Raised when the user aren't authorized to do the action"""
  pass
