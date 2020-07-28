from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from . import add_access_control_headers
from ..wsgi import db
import secrets
import json

from .forms import UploadFileForm

@csrf_exempt
def healthcheck(request):
    if request.method=='GET':
        response = HttpResponse(json.dumps({'status':'get'}), content_type=u"application/json; charset=utf-8")
        return add_access_control_headers(response)

    if request.method=='POST':
        response = HttpResponse(json.dumps({'status':'post'}), content_type=u"application/json; charset=utf-8")
        return add_access_control_headers(response)
    
    else:
        response = HttpResponse("json.dumps({'status':'no'})", content_type=u"application/json; charset=utf-8")
        return add_access_control_headers(response)

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
        response = HttpResponse(json.dumps({'status':'ok'}), content_type=u"application/json; charset=utf-8")
    else:
        response = HttpResponse(json.dumps({'status':'no'}), content_type=u"application/json; charset=utf-8")
    return add_access_control_headers(response)

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)



@csrf_exempt
def endpoint(request):
    if request.method == 'POST':
        print("enter endpoint -1", flush=True)
        raw_data = request.body.decode('utf-8')
        queries = json.loads(raw_data)
        edit_flag = False
        if 'id' in queries:
            edit_flag = True
            item_id = queries['id']
        
        # handle multidict key error
        try:
            a = 10  # TODO
        except:
            response = HttpResponse(json.dumps({'status':'no'}), content_type=u"application/json; charset=utf-8")
            return add_access_control_headers(response)
        
        print("enter endpotin -2", flush=True)

        # handle other tasks
        status = False
        
        # id is in the query
        if edit_flag:
            status = True   # TODO
        # id is not in the query
        else:
            status = True   # TODO
        
        if status:
            response = HttpResponse(json.dumps({'status':'ok'}), content_type=u"application/json; charset=utf-8")
            return add_access_control_headers(response)
        else:
            response = HttpResponse(json.dumps({'status':'no'}), content_type=u"application/json; charset=utf-8")
            return add_access_control_headers(response)

    else:
        response = HttpResponse(json.dumps({'status':'no'}), content_type=u"application/json; charset=utf-8")
        return add_access_control_headers(response)


def query_synthesis(uid, rid):
    try:
        doc_ref = db.collection(u'users').document(uid).collection('results').document(rid)
        doc_ref.set({
            u'video_ready':False
        })
    except:
        return False
    return True

def query_result(uid, rid):
    try:
        doc_ref = db.collection(u'users').document(uid).collection('results').document(rid)
    except:
        return False
    return True

def save_result(uid, result):
    try:
        doc_ref = db.collection(u'users').document(uid).collection('results').document(rid)
        doc_ref.set({
            u'video_ready' : True,
            u'video_result' : result
        })
    except:
        return False
    return True