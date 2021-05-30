from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms

from . import util

import markdown2

class MyForm(forms.Form):
    search_object = forms.CharField()

def index(request):

    query = None

    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search_object"]
            
            entry = util.get_entry(query) 

            if entry:
                return render(request, "encyclopedia/content.html", {
                "name": query.capitalize(),
                "content": markdown2.markdown(entry),
                "form": MyForm()

            })
            else:
                return render(request, "encyclopedia/unknown.html", {
                "name": query,
                "form": MyForm()
                })

    return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries(),
    "form": MyForm(),
    "query": query
    })

def content(request, name):

    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search_object"]
    else:
        query = name

    entry = util.get_entry(query)

    if entry:
        return render(request, "encyclopedia/content.html", {
            "name": query.capitalize(),
            "content": markdown2.markdown(entry),
            "form": MyForm()

        })
    else:
        return render(request, "encyclopedia/unknown.html", {
        "name": query,
        "form": MyForm()
        })

