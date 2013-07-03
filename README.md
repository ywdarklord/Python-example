#Python Example

===============
本例使用Python-SDK 6.0

本Python网页上传工具通过Django框架搭建并使用七牛云存储提供的Python-SDK演示了如何使用Python和Python-SDK开发一个简单的web版文件上传工具样例。
主要内容如下：

安装Django

下载并配置七牛Python-SDK

创建Django项目：一个上传后自动跳转的上传网页和一个下载文件的网页

#安装Django
下载[Django-1.5.1.tar.gz](www.djangoproject.com/download)到本地 运行以下命令执行安装：

     tar xzvf Django-1.5.1.tar.gz
     cd Django-1.5.1
     sudo python setup.py install
#下载并配置Python-SDK
参考此处安装[Python-SDK](github.com/qiniu/python-sdk/blob/develop/docs/README.md)
       
 
#通过Django创建项目
在下面的操作中将会创建一个名为 djproject的项目：
        
        django-admin.py startproject djproject
该语句将在django-admin.py所在的目录中创建一个名为jdproject的目录，进入该项目，可以看到如下几个文件： 

manage.py: 可以使网站管理员来管理Django项目

setting.py: 此Django项目配置文件

urls.py: 包含URL配置文件，用户访问Django应用的方式

###创建一个上传页面应用
使用manage.py 创建一个名为uploader的应用:
        
        manage.py startapp uploader

使用startapp命令后，将会在djproject目录下生成一个uploader目录(如果生成的项目没有位于当前目录下，请将此项目置于与manage.py同一目录下。可一个看到uploader目录下包含：

models.py: 定义数据模型相关信息

tests.py: 该应用的测试文件

views.py: 包含视图相关的信息
这个应用将用于显示上传文件的页面。



####URL设计
在urls.py文件中定义URL。向urls.py中添加如下代码:
            
    urlpatterns = patterns('',

    url(r'^uploader/', 'uploader.views.uploadWithKeyAndCustomField', name='uploadWithKeyAndCustomField'),
    
    
当访问localhost:8000/uploader时，将调用uploader目录下views.py文件中的uploadWithKeyAndCustomField()函数。
####创建视图

配置uploader目录下views.py文件的代码如下：
	
	import qiniu.conf
	import qiniu.rs
	
	from django.http import HttpResponse
	from django.http import HttpResponseRedirect
	
	def uploadWithKeyAndCustomField(request):
	    tokenObj=qiniu.rs.PutPolicy("wyangspace")
	    tokenObj.returnUrl="http://localhost:8000/returnpage"
	    token=tokenObj.token()
	    htmlStr='''<html>
	 <body>
	  <form method="post" action="http://up.qiniu.com/" enctype="multipart/form-data">
	   <input name="token" type="hidden" value="%s">
	   <input name="x:custom_field_name" value="x:me">
	   Image key in qiniu cloud storage: <input name="key" value="foo bar.jpg"><br>
	   Image to upload: <input name="file" type="file"/>
	   <input type="submit" value="Upload">
	  </form>
	 </body>
	</html>'''
	    
	    return HttpResponse(htmlStr %(token))


    
    

这段代码样例，可以指定文件存储到space的文件名，以及用户自定义的custom_field_name. 

七牛API中关于custom_field_name的说明如下：
自定义变量，必须以 x: 开头命名，不限个数。可以在 uploadToken 的 callbackBody 选项中使用 $(x:custom_field_name) 求值。

并且我们还指定了return url, 那么在上传成功之后，浏览器将会跳转至指定的地址而不是显示从up.qiniu.com返回的信息。
    
这样上传文件页面都已经配置完毕。
####启动服务器
   在命令行中，切换到djproject目录，输入如下命令：
         
      manage.py runserver
      
然后访问 http://localhost:8000/uploader/ 

####创建一个上传完成后跳转的页面

我们希望上传完成之后，不仅仅只显示由up.qiniu.com返回的信息，而是希望跳转到一个自定义的页面。这个页面可以显示上传完成后文件的信息。

首先创建一个名为returnpage的项目

    manage.py startapp returnpage
    
并且向刚才的urls.py文件中添加以下内容：

    url(r'^returnpage/', 'returnpage.views.returnPage', name='returnPage')
    
    
 这样当上传完成后，浏览器自动访问localhost:8000/returnpage时，将会调用位于"returnpage"文件夹下view.py中的returnpage()函数。
 
 接下来配置returnpage目录下views.py文件内容如下：
 
	import base64
	import json
	import qiniu.rs
	from django.http import HttpResponse
	from django.http import HttpResponseRedirect
	
	def returnPage(request):
	    domain="YOUR_DOMAIN_HERE(example.qiniudn.com)"
	    ret=request.GET['upload_ret'] #读取返回的upload_ret
	    fileInfo=json.loads(base64.decodestring(ret)) 
	    key=fileInfo['key']
	    base_url=qiniu.rs.make_base_url(domain,key)
	    policy=qiniu.rs.GetPolicy()
	    private_url=policy.make_request(base_url) #获得下载url
	    
	    
	    htmlStr='''
	<html>
	 <body>
	  <p>ImageDownloadUrl: %s
	  <p><a href="/Users">Back to uploadWithkeyAndCustomField</a>
	  <p><img src="%s">
	 </body>
	</html>
	'''
	    return HttpResponse(htmlStr % (private_url,private_url))
	    
	    
这样，我们使用刚才创建的上传页面上传一个图片到七牛后，会自动跳转至此页面，并显示刚才上传好文件的信息，以及图片。


###创建一个下载页面应用

刚才我们完成了一个上传文件的页面。接下来我们创建一个下载图片文件的页面。其中即将用于视图HTML代码如下：

	   <html>
	 <body>
	 <form action="/download/" method="get">
	      Bucket name: <input type="text" name="bucketname" value=""><br> 
	      Filekey download from cloud storage: <input type="text" name="fileKey" value=""><br>
	      Filename saving as: <input type="text" name="fileName" value=""><br>
	      <input type="submit" value="Download">
	  <p>ImageDownloadUrl: %s
	  <p><a href="/Users">Back to uploadWithKey</a>
	  <p><img src="%s">
	 </body>
	</html>
	
	
这个页面可以让用户指定所要获取文件的空间名(bucketname),所要获取的文件名(fileKey)，以及所要另存为的文件名(fileName)。除了fileName外，其他不可为空。

同样的使用命令行创建一个名为"download"的项目：
     
     manage.py startapp download
     
     
 同样的向刚才的urls.py文件中再添加以下内容：
 
    url(r'^download/', 'download.views.download', name='download')
    
 这样当访问localhost:8000/download 时将会调用位于名为"download"文件夹下的views.py文件中的download()函数。
 
 接下来配置download目录下的view.py文件内容如下：
 
	import qiniu.rs
	                             
	                             
	from django.http import HttpResponse
	from django.http import HttpResponseRedirect
	#用于让用户提交需要下载文件的bucket，文件key。如果时图片的话将会显示图片。
	htmlStr='''<html>
	 <body>
	 <form action="/download/" method="get">
	      Domain: <input type="text" name="domainname" value=""><br> 
	      Filekey download from cloud storage: <input type="text" name="fileKey" value=""><br>
	      <input type="submit" value="Download">
	  <p>ImageDownloadUrl: %s
	  <p><a href="/Users">Back to uploadWithKey</a>
	  <p><img src="%s">
	 </body>
	</html>'''
	
	
	def download(request):
	      domain='' #bucket既空间名
	      key=''    #文件的key
	      src=''    #生成的下载URL
	
	      if 'domainname' in request.GET and request.GET['domainname']:
	            domain=request.GET['domainname']
	
	      if 'fileKey' in request.GET and request.GET['fileKey']:
	            key=request.GET['fileKey']
	
	
	      #调用Python-SDK获取下载URL
	      try:
	            base_url=qiniu.rs.make_base_url(domain,key)
	            policy=qiniu.rs.GetPolicy()
	            src=policy.make_request(base_url) 
	      except:
	            pass
	            src='unkown'
	    
	      
	    
	      return HttpResponse(htmlStr % (src,src))
	 
    
     
     
 然后启动服务器，访问localhost:8000/download 即可使用此web下载工具。

   
