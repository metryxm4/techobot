#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
TechoBot
'''

import time
import warnings

warnings.simplefilter('ignore')
import praw
warnings.simplefilter('default')

import itertools
import logic
import requests

from settings import bot_ustring
from settings import subreddits
from settings import submissions
from settings import initial_limit
from settings import loop_limit

from reddit_settings import username
from reddit_settings import password

now = time.time()
print u'[%f] %s' % (now, bot_ustring)

r = praw.Reddit(bot_ustring)
r.login(username, password)

logic.register(r)

r.log('Getting sub', 2)
sub = r.get_subreddit(subreddits)
#sub = r.get_submission(submission_id='1reku2')

r.log('Retrieving comments', 2)
comments = sub.get_comments(limit=initial_limit)
#comments = praw.helpers.flatten_tree(sub.comments)
non_first = False

for submission in submissions:
    comments = itertools.chain(comments, r.get_submission(submission_id=submission).comments)

comments = itertools.chain(comments, r.get_inbox())

if (non_first):
    r.log('Retrieving comments',2)
    comments = sub.get_comments(limit=loop_limit)

non_first = True
caret = '.'

# Single run

for comment in comments:
    caret = '.' if caret == '_' else '_'
    r.log('Processing comment' + caret, 2)
    action = 'none'
    
    if comment.id in r.done:
        continue
    
    if comment.is_command():
        action = comment.process_command()
    
    comment.log(action)

