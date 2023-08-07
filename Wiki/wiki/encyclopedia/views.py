from django.shortcuts import render

from . import util


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
    return render(request, "encyclopedia/create.html")
