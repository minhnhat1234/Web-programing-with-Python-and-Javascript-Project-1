from unicodedata import name
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django import forms
from .models import Entries

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
            return redirect("content", name = query)

    return render(request, "encyclopedia/index.html", {
    "entries": Entries.objects.all(),
    "form": MyForm()
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
        matches_dict = Entries.objects.filter(name__contains = name).values("name")
        matches_list = [entry["name"] for entry in matches_dict]
        print(matches_list)
        print(len(matches_list))
        return render(request, "encyclopedia/unknown.html", {
        "name": name,
        "form": MyForm(),
        "entries": matches_list
        })

