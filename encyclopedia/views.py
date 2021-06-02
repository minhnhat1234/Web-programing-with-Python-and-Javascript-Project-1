from re import search
from unicodedata import name
from wiki.settings import MESSAGE_TAGS
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django import forms
from .models import Entries
from django.contrib import messages

from . import util

import markdown2

class MyForm(forms.Form):
    search_object = forms.CharField()

class EditForm(forms.Form):
    edit = forms.CharField(widget=forms.Textarea, label="")

def index(request):

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

    elif request.GET.get('Edit'):
        return redirect("edit", name = name)

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
        return render(request, "encyclopedia/unknown.html", {
        "name": name,
        "form": MyForm(),
        "entries": matches_list
        })

def edit(request, name):
    if request.method == 'POST':
        if "search_object" in request.POST.values():
            form = MyForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data["search_object"]
                return redirect("content", name = query)
        elif request.POST["edit"]:
            form = EditForm(request.POST)
            if form.is_valid():
                util.save_entry(name, form.cleaned_data["edit"])
                messages.success(request, "Changes saved successfully.")
                return redirect("content", name = name)

    entry = util.get_entry(name)
    if entry:
        initial = {"edit": entry}
        return render(request, "encyclopedia/edit.html", {
        "name": name,
        "form": MyForm(),
        "form_edit": EditForm(initial = initial)
        })
    else:
        return redirect("content", name = name)