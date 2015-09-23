def copy_file(path):
    from os.path import basename, isfile
    assert isfile(path)
    return (basename(path), file(path, 'rb', 0).read())

def paste_file(file_object, path):
    from os.path import isdir, join
    assert isdir(path)
    file(join(path, file_object[0]), 'wb', 0).write(file_object[1])




def copy_dir(path):
    from os import listdir
    from os.path import basename, isdir, isfile, join
    assert isdir(path)
    dir = (basename(path), list())
    for name in listdir(path):
        next_path = join(path, name)
        if isdir(next_path):
            dir[1].append(copy_dir(next_path))
        elif isfile(next_path):
            dir[1].append(copy_file(next_path))
    return dir

def paste_dir(dir_object, path):
    from os import mkdir
    from os.path import isdir, join
    assert isdir(path)
    if dir_object[0] is not '':
        path = join(path, dir_object[0])
        mkdir(path)
    for object in dir_object[1]:
        if type(object[1]) is list:
            paste_dir(object, path)
        else:
            paste_file(object, path)


link='http://mirtarbase.mbc.nctu.edu.tw/php/search.php?opt=species&org=hsa&sort=papers&order=desc&page=1'
import urllib2,urllib
from bs4 import BeautifulSoup
while True:
    print link
    data=urllib2.urlopen(link).read()
    soup=BeautifulSoup(data)
    table=soup.find('table',attrs={'class':'table'})
    tr=table.find_all('tr')
    tr=tr[3:]
    base='http://mirtarbase.mbc.nctu.edu.tw/php/'
    import os
    current_directory=os.getcwd()
    other_directory=current_directory+'\\useful\\'
    print current_directory
    for i in tr:
        try:
            x=i.find('a')
            l=x['href']
            name=l[-10:]
            print name
            final_link=base+l+'#target'
            print final_link
            folder=current_directory+'\\downloads\\'+name
            if not os.path.exists(folder):
                os.makedirs(folder)
            location=folder+'\\'+name+'.html'
            if os.path.isfile(location):
                continue
            data=urllib2.urlopen(final_link).read()
            try:
                soup=BeautifulSoup(data)
            except:
                continue
            
            f=open(location,'w')
            f.write(data)
            f.close()
            location=folder+'\\'+name+'.txt'
            pre=soup.find_all('pre')
            length=(str(pre[0]).split('\n')[-1]).split(' ')
            try:
                for i in length:
                    if i=='':
                        continue
                    else:
                        print i
                        length=int(i)
                        break
            except:
                continue
            print length
            f=open(location,'w')
            f.write(str(pre))
            f.close()
            location=folder+'\\'+name+'_location.txt'
            div=soup.find('div',attrs={'id':'blueDream-in'})
            tbody=div.table.tbody
            tr=tbody.find_all('tr')
            f=open(location,'w')
            for i in tr:
                td=i.find_all('td')[2]
                f.write(str(td))
                f.write('\n')
            f.close()
            if length<500:
                x=copy_dir(folder)
                paste_dir(x,other_directory)
        except:
            continue
    t=link.rfind('=')
    d=int(link[t+1:])+1
    link=link[:t+1]+str(d)
