from django.core.paginator import Paginator, Page
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from .forms import AuthorForm
from .models import Author

from quotes.models import Quote
from tags.models import Tag


# Create your views here.

def main(request):
    quote_list = Quote.objects.all()
    tags = Tag.objects.all()


    TAGS = {}

    for tag in tags:
        TAGS[str(tag.tagname)] = 0

    for quote in quote_list:
        for tag in quote.tags.all():
            TAGS[str(tag.tagname)] += 1

    sorted_tags = sorted(TAGS.items(), key=lambda x: x[1], reverse=True)
    top_ten_tags = sorted_tags[:10]



    paginator = Paginator(quote_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'authors/index.html', {"quote_page": page, 'tags': [top_ten_tag[0] for top_ten_tag in top_ten_tags]})


@login_required
def create_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="authors:main")
        else:
            return redirect(to='authors:create_author')
    return render(request, 'authors/create_author.html', context={'form': AuthorForm})

def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'authors/author.html', {"author": author})