__author__ = 'nnduc_000'

BOT_NAME = 'jobdata'

SPIDER_MODULES = ['scraper_app.spiders']

# Modify this to meet your local database information
'''
DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'nnduc_000',
    'password': 'vip05041994',
    'database': 'scrape'
}

# This one is for our real database server, please use your localhost
# during your programing
'''
DATABASE = {
    'drivername': 'postgres',
    'host': 'web427.webfaction.com',
    'port': '5432',
    'username': 'nnduc1994',
    'password': 'vip05041994',
    'database': 'jobs'
}

ITEM_PIPELINES = ['scraper_app.pipelines.JobDataPipeLine'] # Using for Finland Spider

#ITEM_PIPELINES = ['scraper_app.pipelines.JobDataEstoniaPipeLine'] # Using for Estonia Spider

<input type="submit" value="6" onclick="window.location='open_jobs_view_new.html?_first=101&amp;_rl=2272'">