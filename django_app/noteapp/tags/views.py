from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tag
from .forms import TagForm

from quotes.models import Quote


def tag(request, tagname):
    tag_ = get_object_or_404(Tag, tagname=tagname)
    quotes_with_tag = Quote.objects.filter(tags=tag_)
    return render(request, 'tags/tag.html', context={"tag": tag_, "quotes_with_tag": quotes_with_tag})

@login_required
def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='authors:main')
        else:
            return redirect(to='tags:create_tag')

    return render(request, 'tags/create_tag.html', context={'form': TagForm})