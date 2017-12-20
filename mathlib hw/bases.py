import sqlite3
import matplotlib
import matplotlib.pyplot as plt

gloss = {'1PL':'first person, plural',
         '2PL':'second person, plural',
         '3PL':'third person, plural',
         '1SG':'first person, singular',
         '2SG':'second person, singular',
         '3SG':'third person, singular',
         'ABL':'ablative case',
         'ACC':'accusative case',
         'ADJ':'adjective',
         'ADV':'adverb',
         'AUX':'auxiliary',
         'C':'common gender; complementizer',
         'COMP':'complementizer',
         'CONJ':'conjunction',
         'CONN':'connective',
         'DAT':'dative case',
         'DAT-LOC':'dative-locative case',
         'DEM':'demonstrative pronoun',
         'EMF':'emphatic',
         'EMPH':'emphatic',
         'ENCL':'enclitic',
         'ENLC':'UNKNOWN',
         'GEN':'genitive case',
         'IMF':'UNKNOWN',
         'IMP':'imperative mood',
         'IMPF':'imperfect',
         'INDEF':'indefinite pronoun',
         'INF':'infinitive',
         'INST':'instrumental case',
         'INSTR':'instrumental case',
         'LOC':'locative case',
         'MED':'medium',
         'N':'noun',
         'NEG':'negative',
         'NOM':'nominative case',
         'NUM':'cardinal',
         'P':'preposition (postposition)',
         'PART':'particle',
         'PERS':'personal',
         'POSS':'possessive pronoun',
         'PL':'plural',
         'PRON':'pronoun',
         'PRS':'present tense',
         'PRT':'preterite',
         'PRV':'preverb',
         'PST':'past tense',
         'PTCP':'participle',
         'REFL':'reflexive',
         'REL':'relative pronoun',
         'SG':'singular',
         'Q':'question word',
         'QUOT':'quotative',
         'V':'verb',
         'VOC':'vocative case'}
   gloss2=[]
   for key in gloss:
       gloss2.append(key)
    meaning=[]
    for key in gloss:
        meaning.append(gloss[key])
    for i in mass:
        items=i.split(' — ')
        gloss.append(items[0])
        meaning.append(items[1])
        
conn = sqlite3.connect('hittite.db')
c = conn.cursor()

def sql():
    c.execute('''SELECT Glosses FROM wordforms''')
    g=c.fetchall()
    gl=[]
    for cor in g:
        for gloss in cor:
            glo=g.split('.')
            gl.append(' '.join(glo))

    c.executescript('''DROP TABLE IF EXISTS words;
        CREATE TABLE IF NOT EXISTS words
        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Lemma TEXT,
        Wordform TEXT,
        Glosses TEXT);
        ''')

    c.execute('''INSERT INTO words (Lemma, Wordform, Glosses)
        SELECT Lemma, Wordform, Glosses FROM wordforms;
        ''')

    for i in range(len(gl)):
        c.execute('''
    UPDATE words
    SET Glosses = ?
    WHERE id = ?''', [gl[i], i+1])

    c.executescript('''DROP TABLE IF EXISTS glosses;
        CREATE TABLE IF NOT EXISTS glosses
        (id INTEGER,
        Gloss TEXT,
        Meaning TEXT);
        ''')


    for i in range(1, len(gloss)+1):
        c.execute('INSERT INTO glosses (id, Gloss, Meaning) VALUES (?, ?, ?)',
              [i, gloss[i-1], meaning[i-1]])

    c.executescript('''DROP TABLE IF EXISTS words_glosses;
        CREATE TABLE IF NOT EXISTS words_glosses
        (id_word INTEGER,
        id_gloss INTEGER);
        ''')

    c.execute('SELECT id, Glosses FROM words')
    a = c.fetchall()
    c.execute('SELECT id, Gloss FROM glosses')
    b = c.fetchall()
    for corr in a:
        corr_split=corr[1].split(' ')
        for el in corr_split:
            for item in b:
                if el==item[1]:
                    c.execute('INSERT INTO words_glosses (id_word, id_gloss) VALUES (?, ?)',
                          [corr[0], item[0]])

    c.execute('SELECT id_word FROM words_glosses')
    n=c.fetchall()
    words=[]
    for cor in n:
        for el in cor:
            words.append(el)
    for i in range(1, 528):
        if i in words:
            continue
        else:
            c.execute('INSERT INTO words_glosses (id_word, id_gloss) VALUES (?, ?)',
                  [i, 'No gloss'])
    conn.commit()
    return ()

def pic():
    gr={}
    c.execute('SELECT * FROM words_glosses ORDER BY id_gloss')
    m=c.fetchall()
    for cor in m:
        c.execute('SELECT gloss FROM glosses WHERE id = ?', (cor[1],))
        name=c.fetchall()
        try:
            if name!=[] and name[0][0] in gr:
                gr[name[0][0]]+=1
            else:
                gr[name[0][0]]=1
        except IndexError:
            continue
    plt.title("Glosses from the dictionary")
    for i, key in enumerate(gr):
        plt.scatter(i, gr[key], s=100)
        plt.text(i, gr[key]+1, key)
    return ()

sql() 
pic() 
conn.close()
