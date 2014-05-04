# -*- coding: utf-8 -*-

import re
import math
import pprint

ADMIN_FUNDS_LIMIT = 500
trigger = re.compile(u'(?:\W|^)\+(\d+) +(?:limon|lemon|techo(?:d(?:o|ó))?lar)(?:e?s)?(?:\W|$)', re.I)
subject = re.compile(u'^balance$', re.I)
message = u'\n\n----\n### Techólares, la forma simple y rápida de hacerse güey en [internet](/r/techoblanco)\n\n----\n^\[[balance](/message/compose/?to=techobot&subject=balance)\]'

def triggered_by (comment):
    return True if (hasattr(comment, 'vote') and trigger.search(comment.body)) or (hasattr(comment, 'was_comment') and not comment.was_comment and subject.search(comment.subject)) else False

def run (comment):
    
    # Redditor
    def user_funds (redditor):
        redditor.reddit_session.cursor.execute(
            'SELECT 1, IFNULL(SUM(CASE WHEN target_name=%s THEN amount ELSE -amount END),0) FROM techolars WHERE (source_name=%s OR target_name=%s)',
            (redditor.name.lower(), redditor.name.lower(), redditor.name.lower()))
        funds = redditor.reddit_session.cursor.fetchone()
        funds = int(funds[1]) if funds and funds[0] else float('nan')
        
        return funds
    
    
    # Comment
    def get_amount (comment):
        amount = trigger.search(comment.body)
        amount = int(amount.group(1)) if amount else 0
        
        return amount
    
    def transfer_funds (comment, source, target):
        comment.reddit_session.cursor.execute(
            'INSERT INTO techolars (comment_id,source_name,target_name,amount) VALUES (%s,%s,%s,%s)',
            (
                comment.id,
                source.name.lower(),
                target.name.lower(),
                amount
            )
        )
        comment.reddit_session.db.commit()
    
    
    # Process
    r = comment.reddit_session
    action = 'techolar transaction'
    source = comment.author
    
    r.log('processing comment id %s' % comment.id)
    
    if hasattr(comment,'score'):
        if comment.is_root:
            target = comment.submission.author if comment.submission else None
        else:
            #parent = r.get_submission(comment.permalink.replace(comment.id,comment.parent_id[3:]))
            parent = r.get_info(thing_id=comment.parent_id)
            target = parent.author if parent else None
        
        if not source or not target:
            action = 'invalid techolar transaction'
            return action
        
        if source.name.lower() == target.name.lower():
            comment.reply(u'No tiene caso enviar techólares a tí mismo' + message)
            action = 'same recipient techolar transaction'
            return action
        
        amount = get_amount(comment)
        funds = user_funds(source)
        
        if math.isnan(funds):
            comment.reply((u'/u/%s, el sistema no puede calcular tus fondos para enviar **%s** techólares' + message) % (source.name, amount))
            r.log(u'%s :: /u/%s, el sistema no puede calcular tus fondos (%s) para enviar %s techólares' % (comment.permalink, source.name, funds, amount))
            action = 'funds calculation bug techolar transaction'
            return action
        elif source.name.lower() in comment.reddit_session.mods:
            if amount > funds and amount > ADMIN_FUNDS_LIMIT:
                comment.reply((u'/u/%s, no tienes suficientes fondos para enviar **%s** techólares' + message) % (source.name, amount))
                r.log(u'%s :: Admin /u/%s, no tienes suficientes fondos (%s) para enviar %s techólares' % (comment.permalink, source.name, funds, amount))
                action = 'insufficient admin funds techolar transaction'
                return action
        elif amount > funds:
            comment.reply((u'/u/%s, no tienes suficientes fondos para enviar **%s** techólares' + message) % (source.name, amount))
            r.log(u'%s :: /u/%s, no tienes suficientes fondos (%s) para enviar %s techólares' % (comment.permalink, source.name, funds, amount))
            action = 'insufficient funds techolar transaction'
            return action
        
        # source, target, amount and funds verified, proceed
        r.cursor.execute(
            'INSERT IGNORE INTO techolars (comment_id,source_name,target_name,amount) VALUES (%s,%s,%s,%s)',
            (
                comment.id,
                source.name.lower(),
                target.name.lower(),
                amount
            )
        )
        comment.reddit_session.db.commit()
        
        comment.reply((u'/u/%s, has enviado **%s** techólares a /u/%s' + message) % (source.name, amount, target.name))
        #r.user.send_message(target.name,u'¡Haz recibido techólares!',(u'%s, %s te ha enviado **%d** techólares:\n\n%s' + message) % (target.name, source.name, amount, comment.permalink));
        r.log(u'%s :: /u/%s, has enviado %s techólares a /u/%s' % (comment.permalink, source.name, amount, target.name))
        action = 'techolar transaction'
    elif hasattr(comment,'was_comment') and not comment.was_comment:
        action = 'invalid techolar command'
        
        if subject.search(comment.subject):
            funds = user_funds(comment.author)
            
            if math.isnan(funds):
                comment.reply((u'/u/%s, el sistema no puede calcular tus fondos, estamos trabajando para corregir este error' + message) % (comment.author.name))
                r.log((u'%s :: /u/%s, el sistema no puede calcular tus fondos, estamos trabajando para corregir este error' + message) % (comment.id, comment.author.name))
                action = 'balance bug techolar command'
            else:
                comment.reply((u'/u/%s, tu balance es:\n\n**%s** techólares' + message) % (comment.author.name, funds))
                r.log((u'%s :: /u/%s, tu balance es:\n\n**%s** techólares' + message) % (comment.id, comment.author.name, funds))
                action = 'balance techolar command'
    
    return action
