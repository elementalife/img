#!/usr/bin/env python
# coding: utf-8
import web
from config import settings
from datetime import datetime

from store import Store

render = settings.render
config = settings.config

class UploadView:

    def GET(self):
        return render.upload("Upload")#todos

class Gallery:
    def GET(self):
        return render.gallery("Gallery")
       
class Test:
    def GET(self):
        return render.test()#todos
class Env:
	def GET(self):
		return render._loc
	
class NotFound:
	def GET(self,url):
		print url
		return render.error('您想找的网页不存在',None)

"""
store: image handler
rule: (path) aj/3f/1ow9y7ks8w8s888kswkg8.jpg => (_id) aj3f1ow9y7ks8w8s888kswkg8
if/qp/ceq9shcskssskc888k4.jpg => ifqpceq9shcskssskc888k4

"""

import  os, re

import json

THUMB_PATH = config.thumb_path.rstrip('/')
THUMB_ROOT = config.thumb_root.rstrip('/')
SUPPORTED_SIZE = eval(config.support_size)

def save_file(file, filename):
    import os
    dir_name = os.path.dirname(filename)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name, 0777)
    fp = open(filename, 'wb')
    try:
        fp.write(file.read())
    finally:
        fp.close()

"""
test log
magickwand: 25M
PIL: 12M
shell: 11M
"""
def thumbnail_shell(filename, size_x, distname):
    size = size_x, size_x
    info = identify_shell(filename)
    if info is None:
        return None
    if info['size'] > size:
        print('thumbnail {0} to: {1}'.format(filename, size_x))
        from subprocess import check_call
        check_call(['convert','-thumbnail',str(size_x),filename,distname])
    else:
        from shutil import copyfile
        copyfile(filename, distname)

def identify_shell(imagefile):
    from subprocess import check_output
    try:
        output = check_output(['identify', '-format', '%m %w %h %Q', imagefile])
        info = output.split(' ')
        return {'format': info[0], 'size': (int(info[1]), int(info[2])), 'quality': int(info[3])}
    except CalledProcessError, e:
        print (e)
        return None

def thumbnail_wand(filename, size_x, distname):
    size = size_x, size_x
    from magickwand.image import Image
    im = Image(filename)
    if im.size > size:
        im.thumbnail(size_x)
    im.save(distname)
    del im

def thumbnail_pil(filename, size_x, distname):
    size = size_x, size_x
    from PIL import Image
    im = Image.open(filename)
    if im.size > size:
        im.thumbnail(size, Image.ANTIALIAS)
    im.save(distname, im.format)
    del im

def thumb_image(filename, size_x, distname):
    tt = config.thumb_method
    if tt == 'shell':
        return thumbnail_shell(filename, size_x, distname)
    elif tt == 'wand':
        return thumbnail_wand(filename, size_x, distname)
    elif tt == 'pil':
        return thumbnail_pil(filename, size_x, distname)

#TODO: when cannot find pics return error pic
class Get:
    def GET(self,id1,id2,id3,id4,type):
#		image_url_regex = r'/([a-z0-9]{2})/([a-z0-9]{2})/([a-z0-9]{19,36})(-[sc]\d{2,4})?\.(gif|jpg|jpeg|png)$'
		id = '{0}{1}{2}'.format(id1,id2,id3)
		from store import Store
		store = Store()
		file = store.get(id)
		if file is None:
		    store.close()
		    return render.error("not found",'/')

		org_path = '{0}/{1}/{2}.{4}'.format(id1,id2,id3,id4,type)
		org_file = '{0}/{1}'.format(THUMB_ROOT, org_path)
		if not os.path.exists(org_file):
		    save_file(file, org_file)
		if id4 is None:
		    dst_path = org_path
		    dst_file = org_file
		else:
		    dst_path = '{0}/{1}/{2}{3}.{4}'.format(id1,id2,id3,id4,type)
		    dst_file = '{0}/{1}'.format(THUMB_ROOT, dst_path)
		    #print(ids[3][1:])
		    size = int(id4[2:])
		    if size not in SUPPORTED_SIZE:
		        print('unsupported size: {0}'.format(size))
		        store.close()
		        return render.error("not found",'/')
		    thumb_image(org_file, size, dst_file)
#		print(org_file)
#		print(dst_file)
#		print web.ctx.env
		server_soft = web.ctx.env['SERVER_SOFTWARE']
#		print server_soft
		if server_soft[:5] == 'nginx' and os.name != 'nt':
			print("in")
			store.close()
			#start_response('200 OK', [('X-Accel-Redirect', '{0}/{1}'.format(THUMB_PATH, dst_path))])
			web.header('X-Accel-Redirect', '{0}/{1}'.format(THUMB_PATH, dst_path))
			return ;
		
#		print(file.type) 
		web.header('Content-Type',  str(file.type))
		web.header('Content-Length', '{0.length}'.format(file))
		web.header('Via','store')
		#print(headers)
		
		# TODO: response file content
		distfile = open(dst_file, 'rb')
		data = distfile.read()
		store.close()
		return data; #200OK
		#return [data]
		
		#fd = open(dst_file,'r')
		#return environ['wsgi.file_wrapper'](fd, 4096)
		return render.error("not found",'/')

class Upload:
    def POST(self):
        #print web.ctx.env
        #print web.input()
        #fileName = web.ctx.env['HTTP_X_FILE_NAME']
        file = web.input()['file']
        fileName = web.input()['filename']
#        print file
        from store import Store
        store = Store()
        id = store.store(file, name=fileName)
        store.close()
        if(hasattr(web.input(),'callback')):
        	location = web.input()['callback']+"?"+"("+json.dumps(id)+")"
        	#web.header('Location', location)
        	raise web.redirect(location)
        	#raise web.seeother(location)
        	return "("+json.dumps(id)+")";
#        print file['user_file[]']
#        web.debug(file['user_file'])
#        web.debug(file['user_file'].filename) # 这里是文件名
#        web.debug(file['user_file'].value) # 这里是文件内容
#        web.debug(file['user_file'].file.read()) # 或者使用一个文件对象
#        print file
        return json.dumps(id)
#        return render.error('upload ok!','/')
#        raise web.seeother('/upload')
    
    def GET(self):
        print "here"
        return render.error('您想找的网页不存在','/')

class Url:
	def POST(self):
		#print web.input()
		url = web.input()['url']
		image_url_regex = r'/.*/([^/]+)\.(gif|jpg|jpeg|png)$'
		match = re.search(image_url_regex, url)
		if match is None:
			return json.dumps([False, 'invalid image file'])
		fileName = "{0}.{1}".format(* match.groups())
		#print fileName
		import urllib
		file = urllib.urlopen(url)
		data = file.read()
		store = Store()
		result = store.store(data,name=fileName)
		file.close()
		
		if(hasattr(web.input(),'callback')):
			web.header('Location', web.input()['callback']+"?"+"("+json.dumps(result)+")")
			return "";
		return "("+json.dumps(result)+")"

class Delete:
	def POST(self,id):
		from store import Store
		store = Store()
		data = json.dumps(store.delete(id))
		store.close()
		return data
        
class Browse:
	def GET(self,page_str):
		print page_str
		page = int(page_str)
		limit = 12
		start = 0
		if page < 1:
			page = 1
		start = limit * (page - 1)
		store = Store()
		gallery = store.browse(limit, start)
		if hasattr(store, 'close'):
			store.close()
		import datetime
		dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
		
		result = json.dumps(gallery, default=dthandler)#[] 
		if(hasattr(web.input(),'callback')):
			result = "("+result+")"
			callback= web.input()['callback']
			result = callback + result
			
		return result
