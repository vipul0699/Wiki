from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from markdown2 import Markdown
from django.urls import reverse
import random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,entry):
    if request.method == "GET":
        page = util.get_entry(entry)
        msg = "does not exist"
        if not page:
            err = entry
            return render(request,"encyclopedia/error.html",
            { "ent" : err ,
            "msg" : msg }
            )
        else:
            markdowner = Markdown()
            content = markdowner.convert(page)
            return render(request,"encyclopedia/entry.html",
            { "content" : content ,
            "title" : entry}
            )

def search(request):
    query = request.GET["q"]
    enteries = util.list_entries()
    if query in enteries:
        page = util.get_entry(query)
        markdowner = Markdown()
        content = markdowner.convert(page)
        return render(request,"encyclopedia/entry.html",
        { "content" : content ,
        "title" : query}
        )
    else:
        match_ent = []
        for entry in enteries:
            if query in entry:
                match_ent.append(entry)
        return render(request,"encyclopedia/index.html",
        {"entries":match_ent})

 # Create a page in Markdown
def create(request):
    if request.method == "GET":
        return render(request,"encyclopedia/create.html")
    else:
        content = request.POST["create"]
        title  = request.POST["title"]
        if title in util.list_entries():
            msg = "Already exists in the encyclopedia"
            return render(request,"encyclopedia/error.html",
            {"msg" : msg,
            "ent" : title}) 
        else:
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse("index"))

def Edit(request,entry):
    if request.method == "GET":
        oldpage = util.get_entry(entry)         
        return render(request,"encyclopedia/editor.html",
        {"content": oldpage,
        "title":entry})
    else:                
        util.save_entry(entry,request.POST["edit"])
        markdowner = Markdown()
        return render(request,"encyclopedia/entry.html",
        {"content" : markdowner.convert(request.POST["edit"]),
        "title" : entry})

def ran(request):
    pages = util.list_entries()
    ran_page = random.choice(pages)
    markdowner = Markdown()
    return render(request,"encyclopedia/entry.html",
    {"content" : markdowner.convert(util.get_entry(ran_page)),
     "title" : ran_page})








        



    
    
