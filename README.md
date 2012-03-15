Img: Image storage site
=======================================

Requirements
-----------

 * MongoDB (GridFS)
 * Python + [pymongo][pymongo] + webpy
 * PIL
 * Nginx + [uWSGI][uWSGI]


Launch program
------------------

* mongodb: 

	 mongo localhost/storage

		db.createCollection("img.files",{autoIndexId:false});
		db.img.files.ensureIndex({md5:1},{background:true, unique:true, dropDups:true});

* nginx: add conf/nginx/host.img.conf to nginx.conf

		include conf/nginx/host.img.conf;
		
	vim /etc/hosts
	
		127.0.0.1   img.free4lab.com

* uwsgi: for production

	 start image handle:
		./server_img.sh start

* open url http://img.free4lab.com/

TODO list
---------

- permision control
