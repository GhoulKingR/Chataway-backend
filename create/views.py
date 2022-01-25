from threading import Thread
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from pymongo import MongoClient
import json
from hashlib import sha256

client = MongoClient('localhost', 27017)
db = client['chat']
users = db['users']
names = db['names']
chats = db['chats']

# Create your views here.
@api_view([ 'POST' ])
def create_acc(request):
    data = request.body
    sent = json.loads( data )
    u_name = sent['username']
    pswrd = sent['password']
    out_str = ''

    if (u_name or len(u_name) > 0) and (pswrd or len(pswrd) > 0):
        u_hash = sha256((u_name + pswrd).encode('ASCII')).hexdigest()

        n_obj = { 'name': u_name }

        if names.find_one(n_obj):
            out_str = json.dumps({ 'return': 'already exists' })
        else:
            users.insert_one({ '_id': str(u_hash) })
            names.insert_one(n_obj)
            out_str = json.dumps({ 'return': 'created' })
    else:
        out_str = json.dumps({ 'return': 'invalid' })
    
    return HttpResponse(out_str)

@api_view([ 'POST' ])
def login(request):
    data = request.body
    sent = json.loads( data )
    u_name = sent['username']
    pswrd = sent['password']
    out_str = ''

    if (u_name or len(u_name) > 0) and (pswrd or len(pswrd) > 0):
        u_hash = sha256((u_name + pswrd).encode('ASCII')).hexdigest()
        out_str = 'correct' if users.find_one({ '_id': str(u_hash) }) else 'incorrect'
    else:
        out_str = 'invalid'
    
    return HttpResponse(json.dumps({ 'return': out_str }))

def find_chat(hsh, avails, pos):
    avails[pos] = chats.find_one({ '_id': sha256(hsh.encode('ASCII')).hexdigest() })

def find_availability(contacts):
    contacts_rev = [contacts[1], contacts[0]]
    c_s = [''.join(contacts), ''.join(contacts_rev)]
    avails = [None, None]

    # create 2 threads that search the db for what's in cs
    # and save it to 'avails'
    threads = [Thread(target=find_chat, args=( c_s[j], avails, j)) for j in range(0, 2)]
    for t in threads: t.start()
    for t in threads: t.join()
    
    return avails[0] or avails[1]

@api_view([ 'POST' ])
def get_chat(request):
    contacts = json.loads(request.body)['users']
    available = find_availability(contacts)
    print (available)
    return HttpResponse(json.dumps(available['messages'] if available else []))

@api_view([ 'PUT' ])
def send(request):
    data =  json.loads(request.body)
    contacts = data['users']
    available = find_availability(contacts)
    n_message = data['message']
    
    if available:
        messages = available['messages']
        chats.update_one( {'_id': available['_id'] }, { '$set': {'messages': messages + [n_message] } })
    else:
        chats.insert_one( {'_id': sha256(''.join(contacts).encode('ASCII')).hexdigest(), 'messages': [n_message] } )

    return HttpResponse(json.dumps(n_message))