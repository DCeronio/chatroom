
def findNameFixData(txt, nameList, start):
    end = '\n'
    while True:
        c1 = txt.find(start)
        if c1 == -1:
            break
        c1 = c1 + len(start)
        c2 = txt.find(end, c1)
        name = txt[c1:c2]
        if name not in nameList and start == 'present: ':
            nameList.append(name)
        if start == 'left: ':
            nameList.remove(name)
            print(name + ' left')
        if start == 'joined: ':
            print(name + ' joined')
        txt = txt[:c1-len(start)] +  txt[c2 + len(end):]
        if 'present:\n' in txt:
            txt = txt.replace('present:\n', '', 1)
    return txt, nameList

txt = "left: name1\nleft: bob\njoined: al\n"
nameList = ['name1','name2', 'bob']
txt, nameList = findNameFixData(txt, nameList, 'left: ')
txt, nameList = findNameFixData(txt, nameList, 'joined: ')
print(txt)
print('Present: ', end='')
print(*nameList, sep=', ')

