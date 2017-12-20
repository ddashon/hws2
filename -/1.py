import urllib.request
from urllib import parse
import re
from pymystem import Mystem

m = Mystem()


def weather():
    req = urllib.request.Request('https://yandex.ru/pogoda/10463')
    with urllib.request.urlopen(req) as response:
        code = response.read().decode('UTF-8')
    reg = re.search('<span class="temp__value">(.*?)</span>', code, flags=re.DOTALL)
    w=reg.group(1)
    return w


def main():
    req = urllib.request.Request('https://lenta.ru/')
    with urllib.request.urlopen(req) as response:
        code = response.read().decode('UTF-8')
    text = get.text()
    rus = re.findall('[А-ЯЁа-яё ]{3,}', text)
    new = ' '.join(rus)
    new = re.sub('\s{2,}', '\n', html_clean)
    with open('new.txt', 'w', encoding='UTF-8') as file:
        text = file.write(new)
    return new

def top():
    d = {}
    with open('new.txt', 'w', encoding='UTF-8') as file:
        new = file.read()
    html_lower = new.lower()
    out = html_lower.split()
    for el in out:
        if el in d:
            d[el] += 1
        else:
            d[el] = 1
    val = []
    for el in d:
        val.append(d[el])
    top = []
    for i in range(10):
        im = max(val)
        for a, b in d.items():
            if b == im:
                if a not in top:
                    top.append(a)
                    d.pop(a)
                break
        val.remove(im)
    return top


def parcer(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        code = response.read().decode('Windows-1251')
    s = ''
    for el in data:
        s += str(el) + '\n'
    words = get_text()
    out = words.split('\n')
    output = [] 
    for word in out:
        if '\xa0' not in word and len(word) != 1:
            if word != '' and word != '\xa0' and word != '^':
                only_word = word.split(' ')
                lex = only_word[0].strip(',')
                output.append(lex.strip('\''))
    for i in range(len(output)-1):
        if i%2 == 0:
            with open('dict.csv', 'a', encoding='utf-8') as file:
                text = file.write(output[i] + ',' + output[i+1] + '\n') 
            file.close()
    return


def crawl():
    req = urllib.request.Request('http://www.dorev.ru/ru-index.html?l=c0')
    with urllib.request.urlopen(req) as response:
        code = response.read().decode('Windows-1251')
    reg = re.findall('<a href="(ru-index.html\?l=.*?)">', code)
    links = set(reg)
    for link in links:
        parcer('http://www.dorev.ru/'+link)


def dicts():
    d = {}
    with open('dict.csv', 'r', encoding='utf-8') as file:
        text = file.read()
    out = text.split('\n')
    for el in out:
        outs = el.split(',')
        d[outs[0]] = outs[-1]
    return d

def adj(word1, word2):
    if word1[-3:] == 'еся':
        return [word1[:-3]+'яся', word2]
    else:
        an_word1=m.analyze(word1)
        for el in an_word1:
            if 'analysis' in el:
                analyz1 = el['analysis']
        an_word2 = m.analyze(word2)
        for el in an_word2:
            if 'analysis' in el:
                analyz2 = el['analysis']
        try:
            if 'A' in analyz1[0]['gr'] and 'им' in analyz2[0]['gr']:
                if 'муж' in analyz2[0]['gr']:
                    return [word1, word2]
                else:
                    if 'мн' in analyz1[0]['gr']:
                        return [word1[:-1] + 'я', word2]
                    else:
                        return [word1, word2]
            else:
                return [word1, word2]
        except IndexError:
            return [word1, word2]

def ya(word):
    info = m.analyze(word)
    if 'analysis' in info[0]:
        wordform = info[0]['analysis']
        for arr in wordform:
            if "пр,ед" in arr['gr'] or "дат,ед" in arr['gr']:
                if "A" not in arr['gr']:
                    return word[:-1]+'ѣ'
                else:
                    return word
            else:
                return word
    else:
        return word

def forms(word):
    lemma = m.lemmatize(word)[0]
    if lemma not in dictionary() or len(word) < 2:
        return word
    else:
        found = dictionary()[lemma]
        difference = len(word) - len(found)
        if difference != 0:
            if difference > 0:
                return found[:-difference] + word[-difference-1:]
            else:
                return found
        else:
            if word[-2] == found[-2]:
                return found[:-1]+word[-1:]
            else:
                return found[:-2]+word[-2:]

def translate(word):
    try:
        word = use_of_dict(word)
        vowels = 'йуеиыаоэяюё'
        consonants = 'цкнгшщзхфвпрлджчсмтб'
        for letter in range(len(word)-1): 
            if word[letter] == 'и' and word[letter + 1] in vowels:
                word = word[:letter] + 'i' + word[letter + 1:]
            elif word[letter] == 'И' and word[letter + 1] in vowels:
                word = word[:letter] + 'I' + word[letter + 1:]
        word = yat_dativus(word)
        if word[len(word) - 1] in consonants: 
            word += 'ъ'
        if word.startswith('чрес') or word.startswith('чрес') or word.startswith('черес'):
            word = re.sub('(бе|чре|чере)c', '\\1з', word)
        return word
    except TypeError:
        return word


def alltext():
    with open('output.txt', 'r', encoding='UTF-8') as file:
         text = file.read()
         out = text.split()
    for i in range(0, len(out)-1):
        norm = adj(out[i], out[i + 1])
        out[i], out[i + 1] = norm[0], norm[1] 
        print ('(' + str(i + 1) + '/' + str(len(out)) + ')')
    for i in range(0, len(mass)):
        translated = alltext(out[i])
        if translated != None:
            out[i] = translated
        else:
            out[i] == 'oops'
        print('(' + str(i + 1) + '/' + str(len (out)) + ')')
    print('Готово')
    with open('translated.txt', 'w', encoding='UTF-8') as file:
        text = file.write(' '.join(mass))

def main():
    crawler()
    text_translator()
