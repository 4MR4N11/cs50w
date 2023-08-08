from django.shortcuts import render
from django import forms

from . import util


class CreateForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100, min_length=1)
    content = forms.CharField(label="Content", widget=forms.Textarea)


def search(request, query):
    results = []
    entries = util.list_entries()
    if util.get_entry(query) is not None:
        return (entry(request, query))
    for word in entries:
        if query.lower() in word.lower():
            results.append(word)
    return render(request, "encyclopedia/search.html", {
        "entries": results,
        "query": query
    })


def index(request):
    query = request.GET.get('q', '')
    if query:
        return (search(request, query))
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "entry": util.get_entry(title),
        "title": title
    })


def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None:
                util.save_entry(title, content)
                return entry(request, title)
            else:
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "error": "(*) Entry already exists"
                })
    else:
        return render(request, "encyclopedia/create.html", {
            "form": CreateForm()
        })


def edit(request, title):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return entry(request, title)
    else:
        return render(request, "encyclopedia/edit.html", {
            "form": CreateForm(initial={'title': title, 'content': util.get_entry(title)}),
            "title": title
        })


def random(request):
    import random
    entries = util.list_entries()
    title = random.choice(entries)
    return entry(request, title)
