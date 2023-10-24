from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import AFP_Personnel
from django.http import JsonResponse

# @login_required
def punishment_book(request):
    context = {}
    return render(request, 'book/punishment_book_page.html', context)

# @login_required()
def get_personnel(request):
    """AJAX request to retrieve the personnel's data."""
    # Define the base queryset
    base_query = AFP_Personnel.objects.all()

    # Search term
    search_term = request.GET.get('search[value]', None)
    if search_term:
        base_query = base_query.filter(
            Q(afpsn__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(rank_id__icontains=search_term)
        )

    # Total records
    total_records = base_query.count()

    # Order by
    order_column = int(request.GET.get('order[0][column]', 0))
    order_dir = request.GET.get('order[0][dir]', 'asc')
    order_columns = ['rank_id', 'last_name', 'first_name', 'middle_name', 'afpsn']
    if order_dir == 'asc':
        base_query = base_query.order_by(order_columns[order_column])
    else:
        base_query = base_query.order_by(f'-{order_columns[order_column]}')

    # Page and page length
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    end = start + length

    # Get the data for the current page
    filtered_data = base_query[start:end]

    # Construct the JSON response
    response = {
        'draw': int(request.GET.get('draw', 0)),
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': [
            {'rank_id': item.rank_id,
             'last_name': item.last_name,
             'first_name': item.first_name,
             'middle_name': item.middle_name,
             'afpsn': item.afpsn,
             'actions': f'<button onclick="submitOffense({item.id})"><i class="bi bi-trash"></i> Submit Offense</button>'} for item in
            filtered_data
        ]
    }

    return JsonResponse(response)
