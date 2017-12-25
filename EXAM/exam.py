import os
import re
import os.path 
massiv = [] 
for root, dirs, files in os.walk('C:\\Users\\student\\Desktop\\ex\\thai_pages\\thai_pages'): 
    for f in files: 
        k = os.path.join(root, f) 
        massiv.append(k)
massiv = ['C:\\Users\\student\\Desktop\\ex\\thai_pages\\thai_pages\\187.33.html']

diction={}
import json
for j in massiv: 
    with open (j, 'r', encoding = 'utf-8') as text: 
        text = text.read() 
        reges = re.compile('<tr>.*?<a.*?>.*?<.*?<td>.*?</td></tr>') 
        regthai = re.compile('\'>(.*?)</a>') 
        regengl = re.compile('</td><td class.*?</td><td>(.*?)</td></tr>') 
        kt = re.findall (reges, text)  
        for i in kt: 
            thai = re.search(regthai, i).group(1) 
            engl = re.search(regengl, i).group(1) 
            diction[thai] = engl

with open ('diction.json', 'w', encoding = 'utf-8') as f: 
        json.dump(diction, f, ensure_ascii = False)

back_diction = {} 
for key in diction: 
    back_diction[diction[key]] = key 

with open ('back_diction.json', 'w', encoding = 'utf-8') as f: 
        json.dump(back_diction, f, ensure_ascii = False)
