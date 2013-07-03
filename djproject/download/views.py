# Create your views here.
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
