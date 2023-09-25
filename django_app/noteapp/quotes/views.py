from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import views
from .forms import QuoteForm
from .models import Quote

# Create your views here.
@login_required
def create_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="authors:main")
        else:
            return redirect(to="quotes:create_quote")
    return render(request, 'quotes/create_quote.html', context={'form': QuoteForm})

def quote_detail(request):
    quotes = Quote.objects.all()
    return render(request, 'authors/index.html', {'quotes': quotes})