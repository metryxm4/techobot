# coding=utf-8

import os
import glob
import sys
import imp
import re
import sqlite3 as sqlite
import MySQLdb as mysql

import warnings

warnings.simplefilter('ignore')
import praw
warnings.simplefilter('ignore')

from settings import debug_level
from db_settings import db_controller
from db_settings import db_details

def register (r):
    mods = ['aaroningramn', 'astderek', 'facso', 'fzt', 'cgarcia805', 'monfil']
    
    def extend_classes ():
        # Reddit Session
        def create_tables (r):
            if db_controller is 'sqlite':
                r.cursor.execute('CREATE TABLE IF NOT EXISTS replies (id INTEGER PRIMARY KEY AUTOINCREMENT, comment_id VARCHAR, action VARCHAR)')
                r.cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS comment_id ON replies (comment_id)')
                
                r.cursor.execute('CREATE TABLE IF NOT EXISTS techolars (id INTEGER PRIMARY KEY AUTOINCREMENT, comment_id VARCHAR, source_name VARCHAR, target_name VARCHAR, amount INTEGER)')
                r.cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS comment_id ON techolars (comment_id)')
                
                r.cursor.execute('CREATE TABLE IF NOT EXISTS gmaps (id INTEGER PRIMARY KEY AUTOINCREMENT, comment_id VARCHAR, user_id VARCHAR, lat REAL, lng REAL)')
                r.cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS comment_id ON gmaps (comment_id)')
            elif db_controller is 'mysql':
                r.cursor.execute('CREATE TABLE IF NOT EXISTS replies (id INTEGER AUTO_INCREMENT, comment_id VARCHAR(25), action VARCHAR(255), PRIMARY KEY(id), UNIQUE KEY(comment_id))')
                r.cursor.execute('CREATE TABLE IF NOT EXISTS techolars (id INTEGER AUTO_INCREMENT, comment_id VARCHAR(25), source_name VARCHAR(255), target_name VARCHAR(255), amount INTEGER, PRIMARY KEY(id), UNIQUE KEY(comment_id))')
                r.cursor.execute('CREATE TABLE IF NOT EXISTS gmaps (id INTEGER AUTO_INCREMENT, comment_id VARCHAR(25), user_id VARCHAR(255), lat REAL, lng REAL, PRIMARY KEY(id), UNIQUE KEY(comment_id))')
        
        def load_done_list (r):
            r.done = []
            r.cursor.execute('SELECT comment_id FROM replies')
            
            for each in r.cursor.fetchall():
                r.done.append(each[0])
        
        def load_commands (r):
            r.commands = []
            
            for module in os.listdir('commands'):
                if module[-3:] != '.py':
                    continue
                
                command = imp.load_source(module[:-3], 'commands/' + module)
                r.commands.append(command)
        
        def console_log (r, message, level=1):
            if level <= debug_level:
                if level > 1:
                    print((u'\r\033[K' + message).encode('UTF8')),
                else:
                    print((u'\r\033[K' + message).encode('UTF8'))
                
                sys.stdout.flush()
        # /Reddit Session
        
        # Comment
        def is_command (comment):
            return comment.which_command() is not None
        
        def which_command (comment):
            for command in comment.reddit_session.commands:
                if command.triggered_by(comment):
                    return command
            
            return None
        
        def process_command (comment):
            command = comment.which_command()
            
            if command:
                return command.run(comment)
            
            return 'none'
        
        def comment_log (comment, action):
            r = comment.reddit_session
            
            r.log('INSERT OR IGNORE INTO replies (%s, %s)' % (comment.id, action), 3)
            
            r.done.append(comment.id)
            
            if db_controller is 'sqlite':
                r.cursor.execute('INSERT OR IGNORE INTO replies (comment_id, action) VALUES (%s, %s)', (comment.id, action))
            elif db_controller is 'mysql':
                r.cursor.execute('INSERT IGNORE INTO replies (comment_id, action) VALUES (%s, %s)', (comment.id, action))
            
            r.db.commit()
        # /Comment
        
        setattr(praw.Reddit, 'create_tables', create_tables)
        setattr(praw.Reddit, 'load_done_list', load_done_list)
        setattr(praw.Reddit, 'load_commands', load_commands)
        setattr(praw.Reddit, 'log', console_log)
        
        setattr(praw.objects.Comment, 'is_command', is_command)
        setattr(praw.objects.Comment, 'which_command', which_command)
        setattr(praw.objects.Comment, 'process_command', process_command)
        setattr(praw.objects.Comment, 'log', comment_log)
        
        setattr(praw.objects.Message, 'is_command', is_command)
        setattr(praw.objects.Message, 'which_command', which_command)
        setattr(praw.objects.Message, 'process_command', process_command)
        setattr(praw.objects.Message, 'log', comment_log)
    
    
    if db_controller is 'sqlite':
        db = sqlite.connect('techobot.db')
    elif db_controller is 'mysql':
        db = mysql.connect(host=db_details['host'], user=db_details['user'], passwd=db_details['password'], db=db_details['database'])
    
    cursor = db.cursor()
    
    r.db = db
    r.cursor = cursor
    r.mods = mods
    
    extend_classes()
    
    warnings.simplefilter('ignore')
    r.create_tables()
    warnings.simplefilter('default')
    
    r.load_done_list()
    r.load_commands()
