from functools import wraps
from subprocess import check_output, PIPE

def memoize(function):
  memo = {}

  @wraps(function)
  def wrapper(*args):
    if args in memo:
      return memo[args]
    else:
      rv = function(*args)
      memo[args] = rv
      return rv
  return wrapper


def run(*cmd_args):
  return check_output(cmd_args, stderr=PIPE).decode('utf-8')


