from django.shortcuts import render
import pymongo
from .models import Todo 
from django.conf import settings
from datetime import datetime
# Create your views here.
my_client = pymongo.MongoClient('mongodb://localhost:27017')
dbname = my_client['todolist']
collection_name = dbname["list"]


def index(request):
    return render(request,'index.html')

id_counter = 0
def submit(request):
    global id_counter 
    title = request.GET['title']
    description = request.GET['description']
    priority = request.GET['priority']
    created_at = datetime.now()
    id_counter +=1 

    medicine_2 = {
    'id':id_counter,
    "title": title,
    "description" : description,
    'done':False,
    "priority" : priority,
    'created_at':created_at
    }
    collection_name.insert_many([medicine_2])
    mydictionary = {
        'documents': collection_name.find({}),
    }
    return render(request,'list.html',context=mydictionary)


def list(request):
    mydictionary = {
        'documents': collection_name.find({'done':False}),
    }
    return render(request,'list.html',context=mydictionary)

def sortdata(request):
    mydictionary ={
        "documents" : collection_name.find({'done':False},{}).sort('priority',1)
    }
    return render(request,'list.html',context=mydictionary)

def searchdata(request):
    q = request.GET['query']
    mydictionary = {
        "documents" : collection_name.find({'title':q})
    }
    return render(request,'list.html',context=mydictionary)
    

def delete(request,id):
    delete_data = collection_name.delete_one({'id':id})
    mydictionary = {
        'documents': collection_name.find({}),
    }
    return render(request,'list.html',context=mydictionary)
    
def edit(request, id):
    document = collection_name.find_one({'id': id}) 
    mydictionary = {
        "title": document.get('title', ''),
        "description": document.get('description', ''),
        "priority": document.get('priority', ''),
        "id": document.get('id', '')
    }
    return render(request, 'edit.html', context=mydictionary)

def update(request,id):
    updateTime= datetime.now()
    update_data = collection_name.update_one({'id': id},{'$set':{'title':request.GET['title'],'description':request.GET['description']
    ,'priority':request.GET['priority'],'update_at':updateTime}}) 
    mydictionary = {
        "documents" :collection_name.find({}),
    }
    return render(request,'list.html',context=mydictionary)

def tacheValider(request):
    mydictionary ={
        "documents" : collection_name.find({'done':True})
    }
    return render(request,'validatTache.html',context=mydictionary)

def valider(request, id):
    q = collection_name.find_one({'id': id}, {'_id': 0, 'done': 1})
    update_data = collection_name.update_one({'id': id}, {'$set': {'done': not q['done']}})
    
    mydictionary = {
        "documents": collection_name.find({'done': False}),
    }
    return render(request, 'validatTache.html', context=mydictionary)

