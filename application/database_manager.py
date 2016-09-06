#! usr/bin/env python3

import sqlite3

def create_reviews_table(db):
    cur = db.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS steam_reviews (id serial PRIMARY KEY, url text, date_scraped text, user_recommendation text, user_review_text text, user_name text, user_review_date text);')

def drop_reviews_table(db):
    cur = db.cursor()
    cur.execute('DROP TABLE steam_reviews;')