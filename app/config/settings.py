#!/usr/bin/env python
# coding: utf-8
import web

render = web.template.render('templates/', cache=False)

web.config.debug = True

app_path = '/home/wangchao/workspace/python/img/'
#app_path = '/opt/img/' #for cache dir

config = web.storage(
    email='elementalife@gmail.com',
    site_name = 'IMG',
    site_desc = 'Store and share images',
    static = '/static',

    thumb_path = '/thumb',
    thumb_root = app_path +'cache/thumb/',
    thumb_method = 'pil', #shell, wand, pil
    url_prefix = 'http://127.0.0.1:8080/',
    #url_prefix = 'http://img.free4lab.com/',
	eggs_cache = app_path +'cache/eggs',
	max_file_size = '4096000',
	support_size = '[120,130,160]',
	# for mongodb
    servers = 'localhost',
    db_name = 'storage',
    fs_prefix = 'img',
)

web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render
