import os
import sys
import time
import shutil
import json
import yaml
import random
import math
from frontmatter import Frontmatter
from jinja2 import Environment,FileSystemLoader
import http.server
import socketserver

def handler_from(dir):
    def _init(self, *args, **kwargs):return http.server.SimpleHTTPRequestHandler.__init__(self, *args, directory=self.dir, **kwargs)
    return type(f'HandlerFrom<{dir}>',(http.server.SimpleHTTPRequestHandler,),{'__init__': _init, 'dir': dir})
def server(port):
    with socketserver.TCPServer(("",port),handler_from(dest)) as httpd:
        print("http://localhost:"+str(port))
        try:
            import webbrowser
            webbrowser.open("http://localhost:"+str(port))
        except:None
        try:
            print('ctrl+c to exit')
            httpd.serve_forever()
        except:httpd.server_close()
def other(): # 其他操作
    tmp=sys.argv
    if(".py" in tmp[0]):
        cmd=[]
        for i in tmp:
            if(".py" not in i): cmd.append(i)
    else: cmd=tmp
    if(len(cmd)>0):
        if(cmd[0]=="s" or cmd[0]=="server"):
            if(not os.path.exists(dest)):
                print("请先渲染博客")
                sys.exit()
            port=8000
            if(len(cmd)>1):port=int(cmd[1])
            server(port)
        if(cmd[0]=="n" or cmd[0]=="new"):
            if(len(cmd)<2):
                print("未输入文件名!")
                sys.exit()
            str=cmd[1]
            for i in range(2,len(cmd)): str+=' '+cmd[i]
            info={"date":time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())),"title":str}
            flag=1
            if(os.path.exists("source/_posts/"+str+".md")):
                print("文件已存在,是否覆盖(yes|No)")
                flag=0
                if(input()=="yes"):flag=1
            if(flag):open("source/_posts/"+str+".md","w",encoding='utf-8').write(open("scaffolds/post.md").read().format(**info))
        if(cmd[0]=="np" or cmd[0]=="newpage"):
            if(len(cmd)<2):
                print("未输入文件名!")
                sys.exit()
            str=cmd[1]
            for i in range(2,len(cmd)): str+=' '+cmd[i]
            info={"date":time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())),"title":str}
            flag=1
            if(os.path.exists("source/_pages/"+str+".md")):
                print("文件已存在,是否覆盖(yes|No)")
                flag=0
                if(input()=="yes"):flag=1
            if(flag):open("source/_pages/"+str+".md","w",encoding='utf-8').write(open("scaffolds/page.md").read().format(**info))
        if(cmd[0]=="d" or cmd[0]=="deploy"):
            if not os.path.exists('web'):
                print("请先渲染博客")
                sys.exit()
            ff=0
            if (not os.path.exists('deploy')):                
                os.system("git clone %s deploy"%config['repo'][0])
                ff=1                
            for i in os.listdir('deploy'):
                if '.git' in i: continue
                if os.path.isdir('deploy/'+i): shutil.rmtree('deploy/'+i)
                else: os.remove('deploy/'+i)
            for i in os.listdir('web'):
                if i=='.git': continue
                if os.path.isdir('web/'+i): shutil.copytree('web/'+i,'deploy/'+i)
                else: shutil.copy('web/'+i,'deploy/'+i)

            os.chdir('deploy')
            if(ff):
                open('.gitignore','w',encoding='utf-8').write('.git')
                for i in range(1,len(config['repo'])):
                    os.system("git remote set-url --add origin %s"%config['repo'][i])
            os.system("git add .")
            os.system("git commit -m .")
            os.system("git push -f")

        if(cmd[0]=="h" or cmd[0]=="help" or cmd[0]=="-h" or cmd[0]=="--help"):
            print(
'''
0. 无参数: 渲染博客,生成的文件在web文件夹中
1. [s/server] + [port(端口号,默认8000)]: 在localhost上预览生成的文件
2. [n/new] + [title]: 新建文章
3. [np/newpage] + [title]: 新建页面
4. [d/deploy]: 部署博客
''')
        sys.exit()

def rec(a):
    res=a
    try:res=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.strptime(a,'%Y-%m-%d %H:%M:%S'))
    except:
        try:res=time.strftime('%Y-%m-%dT%H:%MZ',time.strptime(a,'%Y-%m-%d %H:%M'))
        except:
            try:res=time.strftime('%Y-%m-%d',time.strptime(a,'%Y-%m-%d %H'))
            except:return a
            else: return res
        else:return res
    else:return res

class markdown:
    def __init__(self):
        import mistune
        import re
        self.render=mistune.Markdown()
        self.rex=re.sub
    def gen(self,text):
        if config['math']:
            text=self.rex(r'\$+\$+[^\$]+\$+\$',lambda x:'<code><latex_display>%s</latex_display></code>'%x.group(0).replace('<','&lt;').replace('$',''),text)
            text=self.rex(r'\$+[^\$]+\$',lambda x:'<code><latex>%s</latex></code>'%x.group(0).replace('<','&lt;').replace('$',''),text)
        if not t_setting['markdown']:return text
        return self.render(text)
def del_none(a):
    c={}
    for x in a:
        if(a[x]!=None):c.update({x:a[x]})
    return c
def geninfo(dir,file):
    node=Frontmatter.read(open(dir+file,encoding='utf-8').read())
    return {
        **{
            'id':None,
            'origin_addr':file[0:len(file)-3],
            'addr':'/'+file[0:len(file)-3],
            'link':None,
            'pre_link': None,
            'nxt_link': None,
            'pre_title': None,
            'nxt_title': None,
            'title': file[0:len(file)-3],
            'date': time.strftime('%Y-%m-%d %H:%M',time.localtime(os.stat(dir+file).st_mtime)),
            'author': config['author'],
            'tags':[],
            'categories':[],
            'top':0,
            'content':md.gen(node['body']),
            'preview':md.gen(node['body'][0:min(len(node['body']),config['preview_len'])])
        },
        **t_setting['defaut_front'],
        **del_none(node['attributes'])
    }
def topinyin(word):
    res=''
    for i in pypinyin.pinyin(word,style=pypinyin.NORMAL):
        res+=''.join(i)+'-'
    return res[0:len(res)-1].replace(' ','-')

def cmp1(x): # 日期排序
    return str(x['date'])
def cmp2(x): # 置顶
    if(x['top']!=None and x['top']>0):
        return '23333-12-31 '+str(x['top'])
    else: return str(x['date'])

def sort_posts():
    posts.sort(key=cmp1,reverse=True)
    id=tot=len(posts)
    for x in posts: # 按日期编号
        id-=1
        x['id']=id
        if(config['article_address']=='number'):x['addr']='/posts/%d'%id
        else:x['addr']='/posts/'+topinyin(x['title'])
        x['link']=rt+x['addr']
    id=0
    for x in posts: # 获取前后信息
        id+=1
        x['pre_link']=posts[(id-2+tot)%tot]['link']
        x['nxt_link']=posts[id%tot]['link']
        x['pre_title']=posts[(id-2+tot)%tot]['title']
        x['nxt_title']=posts[id%tot]['title']
    posts.sort(key=cmp2,reverse=True)

def gen_index(path,a):
    num=config['page_articles']
    tot=len(a)
    TOT=math.ceil(tot/num)
    res=[]
    for now in range(1,TOT+1):
        nodes=[]
        for i in range((now-1)*num,min(now*num,tot)):nodes.append(a[i])

        pre=path+'/page/%d'%(now-1)
        if(now==1):pre=None
        if(now==2):pre=rt+path+'/'
        nxt=path+'/page/%d'%(now+1)
        if(now==TOT):nxt=None
        if(now==1):addr=path
        else:addr=path+'/page/%d'%now
        
        res.append({
            'id':now,
            'addr':addr,
            'link':rt+addr,
            'title':path,
            'nodes':nodes,
            'pre':pre,
            'nxt':nxt,
        })
    return res

def get_posts():
    for i in os.listdir('source/_posts'):
        if(not i.endswith('.md')): continue
        posts.append(geninfo('source/_posts/',i))
    sort_posts()
    for x in posts:
        for tag in x['tags']:
            if tag in tags:tags[tag].append(x)
            else: tags.update({tag:[x]})
        for node in x['categories']:
            now=categories
            for categorie in node:
                if not 'sub' in now:now.update({'sub':{}})
                if not categorie in now['sub']: now['sub'].update({categorie:{}})
                now=now['sub'][categorie]
            if('nodes' not in now):now.update({'nodes':[x]})
            else: now['nodes'].append(x)
        if os.path.exists('source/_posts/'+x['origin_addr']):
            shutil.copytree('source/_posts/'+x['origin_addr'],dest+x['addr'])
        urls.append([config['site_url']+x['addr'],rec(str(x['date']))])
def get_pages():
    for i in os.listdir('source/_pages/'):
        if(not i.endswith('.md')): continue
        pages.append(geninfo('source/_pages/',i))
    for x in pages:
        urls.append([config['site_url']+x['addr'],rec(str(x['date']))])

def gen_tags():
    for tag in tags:
        index=gen_index('/tags/'+tag,tags[tag])
        for i in index:
            op(dest+i['addr'],template.render(**i,tag=tag,total=len(index)))
            urls.append([config['site_url']+i['addr'],last_build_time])
def gen_categories(path,cates):
    urls.append([config['site_url']+path,last_build_time])
    if 'sub' in cates:
        for cate in cates['sub']:
            gen_categories(path+'/'+cate,cates['sub'][cate])
    if 'nodes' in cates:
        index=gen_index(path,cates['nodes'])
        for i in index:
            op(dest+i['addr'],template.render(**i,path=path,total=len(index),sub=cates['sub'] if 'sub' in cates else None))
    elif 'sub' in cates:
        op(dest+path,template.render(title=path,path=path,sub=cates['sub']))

def gen_pure_data():
    for x in posts:
        pure_data.append({
            'title':x['title'],
            'content':x['content'],
            'link':x['link'],
            'tags':x['tags'],
            'categories':x['categories']
        })
    open(dest+'/pure_data.json',"w",encoding='utf-8').write(json.dumps(pure_data))

def gen_rss():
    import PyRSS2Gen
    rss_items=[]
    for i in pure_data:
        link=config['site_real_rt']+i['link']
        text=i['content'][0:config['preview_len']]
        res=''
        text=text.split('\n\n')
        for x in text: res+='<p>'+x+'</p>'
        res+="<a href=%s target='_blank'>阅读全文</a>"%link
        rss_items.append(PyRSS2Gen.RSSItem(
            title=i["title"],
            link=link,
            description=res,
            guid=PyRSS2Gen.Guid(link)
        ))
    rss=PyRSS2Gen.RSS2(
        title=config['site_name'],
        link=config['site_url'],
        description=config['site_name'],
        lastBuildDate=last_build_time,
        items=rss_items
    )
    rss.write_xml(open(dest+"/atom.xml","w",encoding='utf-8'),encoding='utf-8')
def gen_sitemap():
    a=open(dest+'/sitemap.xml',"w",encoding='utf-8')
    b=open(dest+'/sitemap.txt',"w",encoding='utf-8')
    a.write('''<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n''')
    for i in urls:
        a.write("<url><loc>%s</loc><lastmod>%s</lastmod></url>\n"%(i[0],i[1]))
        b.write(i[0]+'\n')
    a.write("</urlset>")

def baidu_push():
    print("是否百度推送?y|N")
    if input()!="y": return
    import requests
    print("百度推送中……")
    if(os.path.exists('baidu_push_last.txt')):
        oldurls=open("baidu_push_last.txt","r",encoding='utf-8').read()
    else: oldurls=""
    newurls=""
    for i in urls:
       if(not i[0] in oldurls):
           newurls+=i[0]+'\n'
    open("baidu_push_last.txt","w",encoding='utf-8').write(newurls)
    r=requests.post(config["baidu_push"]['url'],files={'file': open('baidu_push_last.txt','rb')})
    print("推送结果:\n%s\n"%r.text)
    open("baidu_push_last.txt","w",encoding='utf-8').write(oldurls+newurls)

def mkdir(path):
    if(not os.path.exists(path)): os.makedirs(path)
def op(path,str):
    mkdir(path)
    open(path+'/index.html',"w",encoding='utf-8').write(str)

def cp(src,dst):
    if(os.path.isdir(src)):
        shutil.copytree(src,dst)
    else:shutil.copyfile(src,dst)

####################################################################################

config=yaml.load(open('config.yml',encoding='utf-8').read())
dest=config['dest']

other()

st_time=time.time()

rt=config['site_rt']
if(config['article_address']=='pinyin'):
    import pypinyin
t_config=yaml.load(open('theme/%s/config.yml'%config['theme'],encoding='utf-8').read())
t_setting=yaml.load(open('theme/%s/setting.yml'%config['theme'],encoding='utf-8').read())
md=markdown()
posts=[]
pages=[]
tags={}
categories={}
pure_data=[]
urls=[]
last_build_time=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.localtime())
env=Environment(loader=FileSystemLoader('theme/%s/layout/'%config['theme']))
env.globals.update(**{
    'config':config,
    't_config':t_config,
    'data':{
        'posts':posts,
        'pages':pages,
        'tags':tags,
        'categories':categories
    },
    'last_build_time': last_build_time
})
env.trim_blocks=True
env.lstrip_blocks=True

if(os.path.exists(dest)): shutil.rmtree(dest)
mkdir(dest)
for i in os.listdir('source'):
    if(i=='_pages' or i=='_posts'):continue
    cp('source/'+i,dest+'/'+i)
for i in t_setting['copy']:
    cp('theme/%s/'%config['theme']+i,dest+'/'+i)

if t_setting['default_render']['posts']:
    get_posts()
    template=env.get_template(t_setting['layout']['post'])
    for i in posts:
        op(dest+i['addr'],env.get_template(t_setting['layout'][i['layout']]).render(**i) if 'layout' in i else template.render(**i))
if t_setting['default_render']['pages']:
    get_pages()
    template=env.get_template(t_setting['layout']['page'])
    for i in pages:
        op(dest+i['addr'],env.get_template(t_setting['layout'][i['layout']]).render(**i) if 'layout' in i else template.render(**i))
if t_setting['default_render']['index']:
    index=gen_index('',posts)
    template=env.get_template(t_setting['layout']['index'])
    for i in index:
        op(dest+i['addr'],template.render(**i,total=len(index)))
if t_setting['default_render']['tags']:
    template=env.get_template(t_setting['layout']['tag_index'])
    gen_tags()
if t_setting['default_render']['categories']:
    template=env.get_template(t_setting['layout']['categories'])
    gen_categories('/categories',categories)

for i in t_setting['extra_render']:
    op(dest+i['path'],env.get_template(t_setting['layout'][i['layout']]).render(title=i['title']))

gen_pure_data()
if config['rss']:gen_rss()
if config['sitemap']:gen_sitemap()

print("finish in %.2fs"%(time.time()-st_time))

if config['baidu_push']['enable']:baidu_push()