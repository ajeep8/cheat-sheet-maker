import os
import sys
import pymongo
import json
from bson import json_util

def sheet2json(sheet):
    a=json.dumps(sheet, sort_keys=True, indent=4, default=json_util.default,ensure_ascii=False)
    print(a)
    print()

def sheet2md(sheet):
    md='---\n'
    md+='author: '+sheet['authorUsername']+'\n'
    md+='title: '+sheet['title']+'\n---\n\n'

    for cell in sheet['cells']:
        md+='# '+cell['title']+'\n\n'
        for row in cell['rows']:
            md+='------\n'+row['lang']+'\n\n'
            #md+='## '+str(row['id']) + ' ' + row['lang']+'\n\n'
            md+=row['value'] + '\n\n'

    f = open('sheets/'+(sheet['authorUsername']+'-'+sheet['title']).replace(" ","")+'.md',"w")
    f.write(md)
    f.close()

def pull(mongoURL):
    client = pymongo.MongoClient("mongodb://root:example@127.0.0.1:27017/")
    print(client.list_database_names())
    db = client.test
    col = db.sheets
    rets = col.find()
    for ret in rets: # 每个sheet是一个ret，ret是词典
        sheet2md(ret)
        #sheet2json(ret)

def md2sheet(f):
    code=False
    meta=True
    metadata={}
    cells=[]
    cell={}
    cell["rowsstr"]=""
    #md=f.read()
    lines=f.readlines()[1:]
    for line in lines:
        #if line=='\n':
        #    continue
        if meta and line=='---\n':
            meta=False
            continue
        if meta:
            m=line.split(': ',1)
            metadata[m[0]]=m[1].strip()
            continue
        if line[0:3]=='```':
            code= not code
            cell["rowsstr"]+=line
            continue
        if line[0:2]=="# " and not code:
            cells.append(cell)
            cell={}
            cell["title"]=line[2:-1]
            cell["rowsstr"]=""
        else:
            cell["rowsstr"]+=line
    cells.append(cell)
    cells.pop(0)

    i=0
    for cell in cells:
        cell['id']=i
        rows=cell['rowsstr'].split('------\n')[1:]
        j=0
        cell['rows']=[]
        for row in rows:
            lang,value=row.split('\n\n',1)
            cell['rows'].append({"id":j,"lang":lang,"value":value})
            j+=1
        del cell['rowsstr']
        i+=1
    return metadata, cells

def push(mongoURL):
    client = pymongo.MongoClient("mongodb://root:example@127.0.0.1:27017/")
    #print(client.list_database_names())
    db = client.test
    col = db.sheets
    rets = col.find()
    for sheet in rets:
        if sheet['title'] != 'test':
            continue
        filename = 'sheets/'+(sheet['authorUsername']+'-'+sheet['title']).replace(" ","")+'.md'
        print(filename)
        try:
            f = open(filename,'r')
    
            meta,cells=md2sheet(f)
            sheet['title']=meta['title'].strip()
            sheet['authorUsername']=meta['author'].strip()
            sheet['cells']=cells
            #print(sheet)
    
            condition={'title': meta['title'], 'authorUsername': meta['author']}
            result = col.update_one(condition, {'$set':sheet})
            #print("Result:",result)
            print("Matched:", result.matched_count)
            exit()
        except ValueError as ret:
            print(ret)

if __name__ == '__main__':
    if len(sys.argv)<2:
        print("python sheetsync.py pull/push mongoURL")
        exit()

    if len(sys.argv)==3:
        mongoURL=sys.argv[2]
    else:
        mongoURL="mongodb://root:example@127.0.0.1:27017/"

    if sys.argv[1]=='pull':
        pull(mongoURL)
    elif sys.argv[1]=='push':
        push(mongoURL)

