#!/usr/bin/env python
# coding: utf-8

pre_fix = 'controllers.'

urls = (
    '/',                     pre_fix + 'img.Gallery', 
    '/upload',               pre_fix + 'img.UploadView',
    
    '/test',                 pre_fix + 'img.Test',
    '/env',                   pre_fix + 'img.Env',
   
#    '/api/get/(\d+)',       pre_fix + 'img.Get',
    r'/([a-z0-9]{2})/([a-z0-9]{2})/([a-z0-9]{19,36})(-[sc]\d{2,4})?\.(gif|jpg|jpeg|png)$',pre_fix + 'img.Get',
    r'/thumb/([a-z0-9]{2})/([a-z0-9]{2})/([a-z0-9]{19,36})(-[sc]\d{2,4})?\.(gif|jpg|jpeg|png)$',pre_fix + 'img.Get',
#    r'/show/([a-z0-9]{2})/([a-z0-9]{2})/([a-z0-9]{19,36})(-[sc]\d{2,4})?\.(gif|jpg|jpeg|png)$'
    '/api/upload',          pre_fix + 'img.Upload',
    '/api/url',             pre_fix + 'img.Url',
    r'/api/url/(\S+)',        pre_fix + 'img.Url',
    r'/api/delete/([a-z0-9]+)' ,        pre_fix + 'img.Delete',
    r'/api/browse/(\d+)' ,        pre_fix + 'img.Browse',
    r'/(.*)',                    pre_fix + 'img.NotFound'
    
    
)
