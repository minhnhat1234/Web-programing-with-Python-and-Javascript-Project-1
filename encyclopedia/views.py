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
from random import randint

class MyForm(forms.Form):
    search_object = forms.CharField()

class EditForm(forms.Form):
    edit = forms.CharField(widget=forms.Textarea, label="")

class Create(forms.Form):
    title = forms.CharField(max_length=100)

def get_random_page():
    content_list = [entry["name"] for entry in Entries.objects.values("name")]
    return content_list[randint(0, len(content_list) - 1)]

def index(request):

    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search_object"]
            return redirect("content", name = query)

    return render(request, "encyclopedia/index.html", {
    "entries": Entries.objects.all(),
    "form": MyForm(),
    "random": get_random_page()
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
            "form": MyForm(),
            "random": get_random_page()
        })
    else:
        matches_dict = Entries.objects.filter(name__contains = name).values("name")
        matches_list = [entry["name"] for entry in matches_dict]
        return render(request, "encyclopedia/unknown.html", {
        "name": name,
        "form": MyForm(),
        "entries": matches_list,
        "random": get_random_page()
        })

def edit(request, name):
    if request.method == 'POST':
        if "search_object" in request.POST.values():
            form = MyForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data["search_object"]
                return redirect("content", name = query)
        elif request.POST.get("edit"):
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
        "form_edit": EditForm(initial = initial),
        "random": get_random_page()
        })
    else:
        return redirect("content", name = name)

def create(request):
    if request.method == 'POST':
        if "search_object" in request.POST.values():
            form = MyForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data["search_object"]
                return redirect("content", name = query)
        elif request.POST.get("title"):
            form = Create(request.POST)
            if form.is_valid():
                name = form.cleaned_data["title"]
                matches_dict = Entries.objects.filter(name__contains = name).values("name")
                matches_list = [entry["name"] for entry in matches_dict]
                if len(matches_list) > 0:
                    messages.warning(request, "The name has already existed, please change the name.")
                    return render(request, "encyclopedia/create.html", {
                    "form": MyForm(),
                    "form_create": Create(),
                    "random": get_random_page()
                    })
                else:
                    return redirect("create_specific", name = name)

    return render(request, "encyclopedia/create.html", {
    "form": MyForm(),
    "form_create": Create(),
    "random": get_random_page()
    })

def create_specific(request, name):
    if request.method == 'POST':
        if "search_object" in request.POST.values():
            form = MyForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data["search_object"]
                return redirect("content", name = query)
        elif request.POST.get("edit"):
            form = EditForm(request.POST)
            if form.is_valid():
                util.save_entry(name, form.cleaned_data["edit"])
                messages.success(request, "Changes saved successfully.")
                # Add data to model
                entry = Entries.objects.create(name = name)
                return redirect("content", name = name)
    matches_dict = Entries.objects.filter(name__contains = name).values("name")
    matches_list = [entry["name"] for entry in matches_dict]
    if len(matches_list) > 0:
        messages.warning(request, "The name has already existed, please change the name.")
        return redirect("create")
    else:
        return render(request, "encyclopedia/create_specific.html", {
        "form": MyForm(),
        "form_create": EditForm(initial={"edit": f"#{name}"}),
        "random": get_random_page()
        })