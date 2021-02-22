from django.shortcuts import render,get_object_or_404, HttpResponseRedirect, reverse
from .models import Article,Category,Comment
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from taggit.models import Tag
from .forms import CommentForm,ArticleForm
from django.views import generic
from django.db.models import Q

# Create your views here.

#Article List
def article_list(request, tag_slug=None):
    
    try:
        article = Article.objects.all()
    except:
        raise Http404("Post Does Not Exist")
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        article = article.filter(tags__in =[tag])

    paginator =Paginator(article,3)
    page_number = request.GET.get('page')
    try:
        article = paginator.page(page_number)
    except PageNotAnInteger:
        article = paginator.page(1)
    except EmptyPage:
        article = page_number.page(paginator.num_pages)
    context = {'article':article, 'tag':tag}
    return render(request, 'webapp/article_list.html', context)


#Article Details
def article_details(request, article):
    article = get_object_or_404(Article, status='published', slug=article)
    comments = article.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = request.article
            new_comment.save()
            return HttpResponseRedirect('/')
    else:
        comment_form = CommentForm()

    context = {'article':article, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form}
    return render(request, 'webapp/article_details.html', context)


def addpost_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES or None)
            if form.is_valid():
                art = form.save(commit=False)
                art.user = request.user
                art.save()
                return HttpResponseRedirect('/accounts/dashboard/')
        else:
            form = ArticleForm()
        return render(request, 'webapp/addpost.html', {'form':form})
    else:
        return HttpResponseRedirect('/accounts/login/')


#Update Post
def updatepost_view(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            art = Article.objects.get(pk=id)
            form = ArticleForm(request.POST, instance=art)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/accounts/dashboard/')
        else:
            art = Article.objects.get(pk=id)
            form = ArticleForm(instance=art)
        return render(request, 'webapp/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/accounts/login/')

#Delete Post
def deletepost_view(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            art = Article.objects.get(pk=id)
            art.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/accounts/login')


class SearchResultsView(generic.ListView):
    model = Article
    template_name = 'webapp/search_result.html'
    
    def get_queryset(self): 
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
        else:
            object_list = self.model.objects.none()
        
        return object_list



def searc(request):
    if 'q' in request.GET:
        q = request.GET['q']
        article =Article.objects.filter(title__icontains=q)
    else:
        article = Article.objects.all()
    context = {'article':article}
    return render(request, 'webapp/article_list.html', context)


def searchposts(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(title__icontains=query) | Q(author__username__icontains=query)

            results= Article.objects.filter(lookups).distinct()

            context={'results': results, 'submitbutton': submitbutton}
            
            return render(request, 'webapp/search.html', context)

        else:
            return render(request, 'webapp/search.html')

    else:
        return render(request, 'webapp/search.html')
