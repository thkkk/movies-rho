from django.shortcuts import render
from .models import *

from django.core.paginator import Paginator
import time

# Create your views here.

def get_pagethings(now_page,tot_page):
    pre2 = 0
    pre1 = 0
    nxt1 = 0
    nxt2 = 0
    if now_page - 2 >= 1:
        pre2 = now_page - 2
    if now_page - 1 >= 1:
        pre1 = now_page - 1

    if now_page + 2 <= tot_page:
        nxt2 = now_page + 2
    if now_page + 1 <= tot_page:
        nxt1 = now_page + 1

    pre = 0
    nxt = 0
    if now_page > 1:
        pre = now_page - 1
    if now_page < tot_page:
        nxt = now_page + 1

    return {
        "pre2": pre2,
        "pre1": pre1,
        "pre": pre,
        "nxt2": nxt2,
        "nxt1": nxt1,
        "nxt": nxt,
        "tot_page": tot_page,
        "now_page": now_page,
    }

def index(request):
    tot = list(Movie.objects.all())
    now_page = 1
    if request.GET.get("page"):
        now_page = int(request.GET.get("page"))
    p = Paginator(tot,18)
    tot_page = p.num_pages
    if now_page > tot_page:
        now_page = tot_page
    if now_page <=0 :
        now_page = 1

    item_list = p.page(now_page).object_list
    context = get_pagethings(now_page,tot_page)
    context["Set_movie"] = item_list
    return render(request,"rho/index.html",context)

def index_actor(request):
    tot = list(Actor.objects.all())
    now_page = 1
    if request.GET.get("page"):
        now_page = int(request.GET.get("page"))
    p = Paginator(tot, 18)
    tot_page = p.num_pages

    item_list = p.page(now_page).object_list
    context = get_pagethings(now_page, tot_page)
    context["Set_actor"] = item_list
    return render(request,"rho/index_actor.html",context)

def movie_page(request,movie_id):
    movie = Movie.objects.get(id=movie_id)
    context = {
        "movie": movie,
        "picture": "/static/rho/image/" + str(movie.id) + ".jpg",
        "comment":movie.comment_set.all(),
        "actors":movie.actor.all(),
    }
    return render(request, "rho/movie_page.html", context)

def actor_page(request,actor_id):
    actor = Actor.objects.get(id=actor_id)
    cpr_times={}
    for mv in actor.movie_set.all():
        for oth_actor in mv.actor.all():
            if cpr_times.__contains__(oth_actor):
                cpr_times[oth_actor]+=1
            else:
                cpr_times[oth_actor]=1
    sorted_actor=sorted(cpr_times.items(), key=lambda item:item[1],reverse=True)

    related_actors=[]
    n=0
    for x in sorted_actor:
        if x[0]==actor:
            continue
        n+=1
        if n <= 10:
            related_actors.append(x)
        else:
            break

    context={
        "actor":actor,
        "photo":"/static/rho/image/actor_"+str(actor.id)+".jpg",
        "movies":actor.movie_set.all(),
        "related_actors":related_actors,
    }
    return render(request,"rho/actor_page.html",context)

def search(request):
    if request.method=="GET" and request.GET:
        keyword = request.GET.get("keyword")
        typ = request.GET.get("typ")
        if typ=="movie" :
            st = time.time()
            movie_tot = set(Movie.objects.filter(name__contains=keyword)).union(set(Movie.objects.filter(actor__name__contains=keyword)))
            #actor_tot = list(set(Actor.objects.filter(movie__name__contains=keyword)))
            ed = time.time()
            #tot = movie_tot + actor_tot
            tot = list(movie_tot)
            now_page = 1
            if request.GET.get("page"):
                now_page = int(request.GET.get("page"))
            p = Paginator(tot, 18)
            tot_page = p.num_pages

            item_list = p.page(now_page).object_list
            context = get_pagethings(now_page, tot_page)

            # Set_movie = Movie.objects.filter(name__contains=keyword)
            # Set_actor = Actor.objects.filter(movie__name__contains=keyword)
            context['Set'] = item_list
            context['keyword']=keyword
            context['typ']=typ
            context['num']=len(tot)
            context['time']=str(round(ed-st,5))+'s'
            return render(request,"rho/search_movie.html",context)
        elif typ == "actor":
            st = time.time()
            actor_tot = set(Actor.objects.filter(name__contains=keyword)).union(set(Actor.objects.filter(movie__name__contains=keyword)))
            #movie_tot = list(set(Movie.objects.filter(actor__name__contains=keyword)))
            ed = time.time()
            #tot = actor_tot + movie_tot
            tot = list(actor_tot)
            now_page = 1
            if request.GET.get("page"):
                now_page = int(request.GET.get("page"))
            p = Paginator(tot, 18)
            tot_page = p.num_pages

            item_list = p.page(now_page).object_list
            context = get_pagethings(now_page, tot_page)

            # Set_movie = Movie.objects.filter(name__contains=keyword)
            # Set_actor = Actor.objects.filter(movie__name__contains=keyword)
            context['Set'] = item_list
            context['keyword'] = keyword
            context['typ'] = typ
            context['num']=len(tot)
            context['time']=str(round(ed-st,5))+'s'
            return render(request, "rho/search_actor.html", context)
        elif typ=="comment":
            st = time.time()
            tot = list(Comment.objects.filter(content__contains=keyword))
            ed = time.time()
            now_page = 1
            if request.GET.get("page"):
                now_page = int(request.GET.get("page"))
            p = Paginator(tot, 18)
            tot_page = p.num_pages

            item_list = p.page(now_page).object_list
            context = get_pagethings(now_page, tot_page)
            context["Set_comment"] = item_list
            context['keyword'] = keyword
            context['typ'] = typ
            context['num']=len(tot)
            context['time']=str(round(ed-st,5))+'s'
            return render(request, "rho/search_comment.html", context)