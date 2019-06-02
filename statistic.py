import configparser
import datetime
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

config = configparser.ConfigParser()
config.read('config.ini')

log_file = config['FILES']['LOG_FILE']

def send_stat(period, statistic):
    types = ['type', 'id', 'username', 'firstname', 'lastname', 'group id', 'group name', 'country code', 'date', 'service', 'query']
    log = pd.DataFrame(columns=types)
    
    with open(log_file, 'r', encoding='utf-8-sig') as f:
        for line in f:
            log_el = line.split(' | ')
            row = np.array(log_el)
            df = pd.DataFrame([row], columns=types)
            log = log.append(df, ignore_index=True)

    log['date'] = pd.to_datetime(log['date'], format=("%d.%m.%Y %H:%M"))
        
    return get_stat(log, period, statistic)

def get_stat(log, period, statistic):
    
    now = pd.Series(datetime.datetime.now()).dt
  
    periods = {
        'month': log[log['date'].dt.dayofyear >= int(now.dayofyear) - 30],
        'last_month': log[log['date'].dt.month == int(now.month) - 1],
        'week': log[log['date'].dt.dayofyear >= int(now.dayofyear) - 7],
        'last_week': log[log['date'].dt.week == int(now.week) - 1],
        'yesterday': log[log['date'].dt.dayofyear == int(now.dayofyear) - 1]
    }
  
    #с этим дублем что то сделать
    if period != 'all':
        per = periods[period]
    else:
        per = log
    ###
        
    if not per.empty:
        if statistic == 'uniq':
            df = per.groupby([log["date"].dt.date, 'id']).id.count().reset_index(name='counts').groupby('date').count().drop('counts', axis=1)
            fig = df.plot(kind="bar", grid=True, color='red', legend=False, figsize=[7, 3]).set_xlabel('').get_figure()
            
        elif statistic == 'news':
            user_first = get_new_users(log)
            news = pd.DataFrame.from_dict(user_first, orient='index', columns=['date']).reset_index()
            if period != 'all':
                if period == 'month': per = 30
                elif period == 'week': per = 7
                news = news[news['date'].dt.dayofyear >= int(now.dayofyear) - per]
                
            if not news.empty:
                df = news.groupby(news['date'].dt.date).agg({'index': 'count'})
                fig = df.plot(kind="bar", grid=True, color='red', legend=False, figsize=[7, 3]).set_xlabel('').get_figure()
            else: 
                return 'На твоего унылого бота не подписывались'
 
        else:
            if statistic == 'count':
                df = per.groupby(log['date'].dt.date).agg({"query": "count"})
            else:
                df = per.groupby(log[statistic]).agg({"query": "count"})
            fig = df.plot(kind="bar", grid=True, color='red', legend=False, figsize=[7, 3], ).set_xlabel('').get_figure()
            
        fig.suptitle('{} {}'.format(period, statistic))
        plt.style.use('dark_background')
        return fig.savefig('daily_queries.png', bbox_inches='tight') 
    return 'Твоим унылым ботом не пользовались'

def get_new_users(log):
    user_first = {}
    users = {}
    for idx, row in log.iterrows():
        if row['type'] == 'private' and row['id'] != '1111111111' and row['id'] not in users:
            users[row['id']] = [row['username'], row['firstname'], row['lastname']]
            user_first[row['id']] = row['date']
    return user_first