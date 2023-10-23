from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def punishment_book(request):

    context = {
    }
    return render(request, 'book/punishment_book_page.html', context)
