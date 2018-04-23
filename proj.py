import urllib.request
import json
import sqlite3
import matplotlib.pyplot as plt


def download():
    offsets = [0, 100, 200, 300]
    conn = sqlite3.connect('vkapi.db')
    c = conn.cursor()
    c.executescript("""DROP TABLE IF EXISTS posts;
                            CREATE TABLE posts
                            (post_id TEXT, 
                             post TEXT);
                    """)
    for off in offsets:
        req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-88350989&v=5.74&access_token=533bacf01e11f55b536a565b57531ad114461ae8736d6506a3&count=100&offset=' + str(off))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        data = json.loads(result)
        for item in data['response']['items']:
            c.execute('''
                    INSERT INTO posts (post_id, post) 
                    VALUES (?, ?)
                        ''', [item['id'], item['text']])
    conn.commit()
    conn.close()


def getcomms():
    conn = sqlite3.connect('vkapi.db')
    c = conn.cursor()
    c.executescript("""
                        DROP TABLE IF EXISTS comments;
                        CREATE TABLE comments
                                (post_id TEXT,
                                 comment TEXT, 
                                 user_id TEXT);
                        """)
    c.execute('''SELECT post_id
                 FROM posts ''')
    result = c.fetchall()
    for i in result:
        offsets = [0, 100, 200]
        for off in offsets:
            req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-88350989&post_id=' + i[0] + '&v=5.74&access_token=533bacf01e11f55b536a565b57531ad114461ae8736d6506a3&count=100&offset=''' + str(off))
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf-8')
            data = json.loads(result)
            for item in data['response']['items']:
                c.execute('''
                        INSERT INTO comments (post_id, comment, user_id) 
                        VALUES (?, ?, ?)
                            ''', [i[0], item['text'], item['from_id']])
    conn.commit()
    conn.close()


def getinf(): 
    conn = sqlite3.connect('vkapi.db')
    c = conn.cursor()
    c.executescript("""
                            DROP TABLE IF EXISTS socio;
                            CREATE TABLE socio
                                    (user_id TEXT,
                                     comment_length TEXT, 
                                     city TEXT,
                                     age TEXT);
                            """)
    c.execute('''SELECT user_id, comment
                     FROM comments ''')
    result = c.fetchall()
    for el in result:
        comment_length = len(el[1])
        if el[0][0] == '-':
            usrid = el[0][1:]
        else:
            usrid = el[0]
        req = urllib.request.Request(
            'https://api.vk.com/method/users.get?user_id=' + usrid + '&fields=bdate,city&v=5.74&access_token=533bacf01e11f55b536a565b57531ad114461ae8736d6506a3')
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        data = json.loads(result)
        try:
            date = data['response'][0]['bdate']
            date = date.split('.')
            if len(date[-1]) == 4:
                age = 2018 - int(date[-1])
            else:
                age = ''
        except KeyError:
            age = ''
        try:
            city = data['response'][0]['city']['title']
        except KeyError:
            city = ''
        c.execute('''
                     INSERT INTO socio (user_id, comment_length, city, age) 
                     VALUES (?, ?, ?, ?)
                     ''', [usrid, comment_length, city, age])
    conn.commit()
    conn.close()


