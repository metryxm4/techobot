# -*- coding: utf-8 -*-

import re
import urllib
import json

subject = re.compile(u'^estoy en$', re.I)
message = u'\n\n----\n### Techoblanqueños en el mapa\n\n----\n^\[[ubicación](/message/compose/?to=techobot&subject=estoy+en&message=ciudad,+estado,+país)\]'

def triggered_by (comment):
    return True if (hasattr(comment, 'was_comment') and not comment.was_comment and subject.search(comment.subject)) else False

def run (comment):
    def find_location (address):
        try:
            data = urllib.urlopen('http://maps.google.com/maps/api/geocode/json?sensor=false&address=' + urllib.quote_plus(address.encode('utf8'))).read()
            response = json.loads(data)
            
            if response['status'] == u'OK':
                return response['results'][0]['geometry']['location']
        except:
            return None
        
        return None
    
    def update_location (user, location):
        comment.reddit_session.cursor.execute('SELECT user_id FROM gmaps WHERE user_id=%s', (user.name.lower(),))
        current = comment.reddit_session.cursor.fetchone()
        
        if current:
            comment.reddit_session.cursor.execute('UPDATE gmaps SET comment_id=%s, lat=%s, lng=%s WHERE user_id=%s', (comment.id, location['lat'], location['lng'], user.name.lower()))
        else:
            comment.reddit_session.cursor.execute('INSERT INTO gmaps (comment_id, user_id, lat, lng) VALUES (%s, %s, %s, %s)', (comment.id, user.name.lower(), location['lat'], location['lng']))
        
        comment.reddit_session.db.commit()
    
    def publish_gmap ():
        return None
    
    # Process
    r = comment.reddit_session
    action = 'invalid gmaps command'
    source = comment.author
    
    r.log('processing comment id %s' % comment.id)
    
    if hasattr(comment,'was_comment') and not comment.was_comment and subject.search(comment.subject):
        location = find_location(comment.body)
        
        if location is None:
            comment.reply((u'/u/%s, no fue posible procesar la dirección' + message) % (comment.author.name))
            r.log((u'%s :: /u/%s, no fue posible procesar la dirección' + message) % (comment.id, comment.author.name))
            action = 'unsuccessful locate gmaps command'
        else:
            update_location(comment.author, location)
            
            comment.reply((u'/u/%s, tus coordenadas son: **%s**, **%s**\n\n%s\n\n' + message) % (comment.author.name, location['lat'], location['lng'], re.sub('^','> ', comment.body, re.M)))
            r.log((u'%s :: /u/%s, tus coordenadas son: **%s**, **%s**\n\n%s\n\n' + message) % (comment.id, comment.author.name, location['lat'], location['lng'], re.sub('^', '> ', comment.body,re.M)))
            action = 'locate gmaps command'
    
    return action
