# Create your views here.
# Create your views here.
#import sys
#sys.path.append('/Users/yangwang/python-sdk-3.0.0/qbox')
#import uptoken

                             
                             
from django.http import HttpResponse
from django.http import HttpResponseRedirect

def returnPage(request):
    htmlStr='''
<html>
 <body>
  <p>%s
  <p>ImageDownloadUrl: %s
  <p><a href="/upload">Back to upload</a>
  <p><a href="/upload2">Back to uploadWithKey</a>
  <p><a href="/Users">Back to uploadWithkeyAndCustomField</a>
  <p><img src="%s">
 </body>
</html>
'''
    return HttpResponse(htmlStr)
