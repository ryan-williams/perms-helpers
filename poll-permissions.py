#!/usr/bin/env python

from dataclasses import dataclass
from pathlib import Path
from re import match, Match
from subprocess import check_output as run

@dataclass
class ACL:
  r: bool
  w: bool
  x: bool

  regex = r'(?P<r>r)?(?P<w>w)?(?P<x>x)?'

  @classmethod
  def from_acl(cls, acl):
    if isinstance(acl, str):
      m = match(cls.regex, acl)
    elif isinstance(acl, Match):
      m = acl
    else:
      raise ValueError(f'Unrecognized ACL: {acl}')

    return ACL(*[bool(m[k]) for k in 'rwx'])


@dataclass
class Permission:
  u: ACL
  g: ACL
  o: ACL

  regex = f'(?P<u>u)?(?P<g>g)?(?P<o>o)?\+{ACL.regex}'

  @classmethod
  def from_permissions(self, permissions):
    if isinstance(permissions, str):
      permissions = [ permissions ]
    for



def main(sleep, permissions, paths):
  if isinstance(permissions, str):
    permissions = [ permissions ]
  matches = [
    match(r'(?P<u>u)?(?P<g>g)?(?P<o>o)?\+(?P<r>r)?(?P<w>w)?(?P<x>x)?', s).groupdict(None)
    for s in permissions
  ]

  #perms = match(r'(?P<u>u)?(?P<g>g)?(?P<o>o)?\+(?P<r>r)?(?P<w>w)?(?P<x>x)?', permissions).groupdict(None)
  who = perms
  regex = r'(?:(?P<r>[r\-])(?P<w>[w\-])(?P<x>[x\-]){3}'
  while True:
    lines = run(['stat','-c','%A',] + [ str(path) for path in paths ]).decode().split('\n')
    lines = [ match(regex, line.strip()) for line in lines ]


    # stat -c '%A' . | grep -q 'r-x$'
    # echo "`date +%Y-%m-%dT%H:%M:%S`: o+rx"
    # (echo "`date +%Y-%m-%dT%H:%M:%S`: `stat -c '%A'`"; break)
    # sleep 60

if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('-s', '--sleep', default=60, type=int, help='Time to sleep in between checking permissions')
  parser.add_argument('-p', '--permissions', nargs='*', default='o+rx', help='Permissions to verify that <path>(s) posess')
  parser.add_argument('path', nargs='*', help='Path(s) to monitor permissions for')

  args = parser.parse_args()
  sleep = args.sleep
  permissions = args.permissions
  paths = args.path
  if paths:
    paths = [ Path(path) for path in paths ]
  else:
    paths = [ Path.cwd() ]

  permissions = [
    permission
    for s in permissions
    for permission in s.split(',')
  ]

  main(sleep, permissions, paths)
