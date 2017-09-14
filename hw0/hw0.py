import urllib.request 
req = urllib.request.Request('http://selskie-zori.com/')
with urllib.request.urlopen(req) as response:
   html = response.read().decode('utf-8')
import re
regPostTitle = re.compile('<li class="b-page-header__menu__list__item"><a href="/.*?/">.*?</a></li>', flags= re.DOTALL)
titles = regPostTitle.findall(html)
new_titles = []
regTag = re.compile('<.*?>', re.DOTALL)
regSpace = re.compile('\s{2,}', re.DOTALL)
for t in titles:
    clean_t = regSpace.sub("", t)
    clean_t = regTag.sub("", clean_t)
    new_titles.append(clean_t)
with open ('selo.txt', 'w', encoding = 'utf-8') as f:
    for t in new_titles:
        f.write(t)
