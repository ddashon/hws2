import urllib.request, re, os

def download_page(pageUrl):
    page = urllib.request.urlopen(pageUrl)
    text = page.read().decode('utf-8')
    return text
def form (html):
    html_content = '<html>...</html>'  
    regTag = re.compile('<.*?>', re.DOTALL) 
    regScript = re.compile('<script>.*?</script>', re.DOTALL) 
    regComment = re.compile('<!--.*?-->', re.DOTALL)  
    clean_t = regScript.sub("", html)
    clean_t = regComment.sub("", clean_t)
    clean_t = regTag.sub("", clean_t)
    return clean_t   
os.mkdir ('files')
os.mkdir ('myst')
os.mkdir ('xml')
commonUrl = 'http://www.kurer-sreda.ru/'
namefile = '{0}.txt'
for i in range(2014, 2017):
    pageUrl = commonUrl + str(i) + '/'
    name= str(i)
    if not os.path.exists(name):
        os.mkdir (os.path.join('files', name))
        os.mkdir (os.path.join('myst', name))
        os.mkdir (os.path.join('xml', name))
    for q in range (1, 13):
        pageUrl2 = commonUrl + str(q) + '/'
        name2 = str (q)
        if not os.path.exists(name2):
            os.mkdir (os.path.join('files', name, name2))
            os.mkdir (os.path.join('myst', name, name2))
            os.mkdir (os.path.join('xml', name, name2))
        for w in range (1, 32):
            pageUrl3 = commonUrl + str(w) + '/'
            name3= str (w)
            if not os.path.exists(name3):
                os.mkdir (os.path.join('files', name, name2, name3))
                os.mkdir (os.path.join('myst', name, name2, name3))
                os.mkdir (os.path.join('xml', name, name2, name3))
            print(pageUrl3)
            a=download_page(pageUrl3)
            b=form(a)
            with open (os.path.join('files', name, name2, name3,namefile.format(str(q))), 'w', encoding='utf-8') as f:
                f.write(b)
def my ():
    s=r"mystem.exe"
    for root, dirs, files in os.walk ('files'):
        for file in files:
            st = root.replace('files', 'myst')
            os.system(r"mystem.exe" + ' ' + 'files' + os.sep + file + ' ' +  st + os.sep + file + ' -cid --format text')

def myxml ():
    s=r"mystem.exe"
    for root, dirs, files in os.walk ('files'):
        for file in files:
            st = root.replace('files', 'xml')
            os.system(r"mystem.exe" + ' ' + 'files' + os.sep + file + ' ' +  st + os.sep + file + ' -cid --format xml')

my()
myxml()

