# coding=utf-8

import re
import random

trigger = re.compile(u'(\W|^)/u/techobot(\W|$)',re.I)
responses = (u'¿Qué, qué, yo qué?', u'Me zumbaron los oídos.', u'[Dime](/extrapalapaquetl)')

def triggered_by (comment):
    triggered = trigger.search(comment.body)
    return True if triggered and hasattr(comment, 'vote') else False

def run (comment):
    r = comment.reddit_session
    action = 'mention'
    
    if comment.is_root:
        author = comment.submission.author.name.lower() if comment.submission else None
    else:
        #parent = r.get_submission(comment.permalink.replace(comment.id,comment.parent_id[3:]))
        parent = r.get_info(thing_id=comment.parent_id)
        author = parent.author.name.lower() if parent else None
    
    if author == r.user.name.lower():
        return action
    
    if random.randint(0,1):
        comment.reply(random.sample(responses, 1)[0])
        r.log('%s :: Respondiendo a /u/%s' % (comment.permalink, comment.author.name if comment.author else '[deleted]'))
        action = 'answered mention'
    
    return action
