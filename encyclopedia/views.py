from unicodedata import name
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django import forms

from . import util

import markdown2

class MyForm(forms.Form):
    search_object = forms.CharField()

entries = util.list_entries()

def index(request):

    query = None

    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search_object"]
            return redirect("content", name = query)

    return render(request, "encyclopedia/index.html", {
    "entries": entries,
    "form": MyForm(),
    "query": query
    })

def content(request, name):

    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search_object"]
            return redirect("content", name = query)

    entry = util.get_entry(name)

    if entry:
        return render(request, "encyclopedia/content.html", {
            "name": name.capitalize(),
            "content": markdown2.markdown(entry),
            "form": MyForm()

        })
    else:
        matches = filter(entries, name_contained = name)
        return render(request, "encyclopedia/unknown.html", {
        "name": name,
        "form": MyForm(),
        "entries": matches
        })

