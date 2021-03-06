#! usr/bin/env python3

'''
This module handles the interaction between the database and the rest of this program.
'''

import sqlite3

def create_steam_reviews(d_base_location):
    with sqlite3.connect(d_base_location, timeout=20) as d_base:
        cur = d_base.cursor()
        query = '''CREATE TABLE IF NOT EXISTS steam_reviews (id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT, app_num INTEGER, date_scraped TEXT, classified INTEGER,
        user_recommendation TEXT, user_review_text TEXT, user_name TEXT);'''
        cur.execute(query)

def drop_steam_reviews(d_base_location):
    with sqlite3.connect(d_base_location, timeout=20) as d_base:
        cur = d_base.cursor()
        cur.execute('DROP TABLE steam_reviews;')

def insert_data_steam_reviews(d_base_location, url, app_num, date_scraped, classified,
                              user_recommendation, user_review_text, user_name):
    '''
    Used by scraper to enter data to d_base.
    '''

    with sqlite3.connect(d_base_location, timeout=20) as d_base:
        cur = d_base.cursor()
        query = '''INSERT INTO steam_reviews (url, app_num, date_scraped, classified,
        user_recommendation, user_review_text, user_name) VALUES (?,?,?,?,?,?,?);'''
        data = (url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name)
        cur.execute(query, data)
        d_base.commit()

def remove_duplicates_steam_reviews(d_base_location):
    '''
    In theory, we should never need to do this, because the scraper would
    filter out any duplicates as it goes. This can be done to make sure
    there are no duplicates if concerned the scraper hasn't worked.
    This may be useful to test that scraper functionality has worked.
    '''

    with sqlite3.connect(d_base_location, timeout=20) as d_base:
        cur = d_base.cursor()
        query = '''DELETE FROM steam_reviews WHERE id NOT IN (SELECT MAX(id) FROM steam_reviews
        GROUP BY user_name, user_recommendation, user_review_text);'''
        cur.execute(query)
        d_base.commit()

def retrieve_steam_reviews(d_base_location, user_recommendation, classified, review_quantity):
    '''
    Retrives reviews for classification. Consider adding an argument to retrieve x amount.
    '''

    with sqlite3.connect(d_base_location, timeout=20) as d_base:
        cur = d_base.cursor()
        query = '''SELECT * FROM steam_reviews WHERE user_recommendation=? AND classified=?
        ORDER BY id DESC LIMIT ?;'''
        data = (user_recommendation, classified, review_quantity)
        cur.execute(query, data)
        return cur.fetchall()

def retrieve_last_steam_review(d_base_location):
    '''
    Gets the last review. Currently used to determine the last scraped review,
    to continue the scraping.
    '''

    with sqlite3.connect(d_base_location, timeout=20) as d_base:
        cur = d_base.cursor()
        query = 'SELECT * FROM steam_reviews ORDER BY id DESC LIMIT 1;'
        cur.execute(query)
        return cur.fetchone()

