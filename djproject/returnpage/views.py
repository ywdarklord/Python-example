# Create your views here.
# Create your views here.

                             
import base64
import json
import qiniu.rs
from django.http import HttpResponse
from django.http import HttpResponseRedirect

def returnPage(request):
    domain="wyangspace.qiniudn.com"
    ret=request.GET['upload_ret']
    fileInfo=json.loads(base64.decodestring(ret))
    key=fileInfo['key']
    base_url=qiniu.rs.make_base_url(domain,key)
    policy=qiniu.rs.GetPolicy()
    private_url=policy.make_request(base_url)
    
    
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
