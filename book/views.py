from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import (
    AFP_Personnel, OffenseLibrary, PlaceOfOmission, Offense, PunishmentLibrary
)
from django.http import JsonResponse
from book.utils.date_formatter import date_formatter2

# @login_required
def submission_page(request):
    context = {}

    return render(request, 'book/submission_page.html', context)

def personnel_violation_page(request):
    context = {}
    return render(request, 'book/submitted_offense_page.html', context)


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
    length = int(request.GET.get('length', 5))
    end = start + length

    # Get the data for the current page
    filtered_data = base_query[start:end]

    # Construct the JSON response
    response = {
        'draw': int(request.GET.get('draw', 0)),
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': [
            {
                'rank_id': item.rank_id,
                'last_name': item.last_name,
                'first_name': item.first_name,
                'middle_name': item.middle_name,
                'afpsn': item.afpsn,
                'actions': '<button type="button" onclick="addPersonnel(' + str(
                    item.id) + ', \'' + item.rank_id + '\', \'' + item.first_name + '\', \'' + item.middle_name + '\', \'' + item.last_name + '\', \'' + item.afpsn + '\')" class="btn btn-sm btn-info mr-auto">Select</button>'
            } for item in filtered_data
        ]
    }
    return JsonResponse(response)


def get_offense(request):
    """AJAX request to retrieve the personnel's data."""
    # Define the base queryset
    base_query = OffenseLibrary.objects.all()

    # Search term
    search_term = request.GET.get('search[value]', None)
    if search_term:
        base_query = base_query.filter(
            Q(violation__icontains=search_term)
        )

    # Total records
    total_records = base_query.count()

    # Order by
    order_column = int(request.GET.get('order[0][column]', 0))
    order_dir = request.GET.get('order[0][dir]', 'asc')
    order_columns = ['violation']
    if order_dir == 'asc':
        base_query = base_query.order_by(order_columns[order_column])
    else:
        base_query = base_query.order_by(f'-{order_columns[order_column]}')

    # Page and page length
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 5))
    end = start + length

    # Get the data for the current page
    filtered_data = base_query[start:end]

    # Construct the JSON response
    response = {
        'draw': int(request.GET.get('draw', 0)),
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': [
            {
                'id': item.id,
                'violation': item.violation,
                'actions': f'<button type="button" onclick="addViolations({item.id}, {item.violation})" class="btn btn-sm btn-info mr-auto">Use</button>'
            } for item in filtered_data
        ]
    }

    return JsonResponse(response)

def get_punishments(request):
    """AJAX request to retrieve the personnel's data."""
    # Define the base queryset
    base_query = PunishmentLibrary.objects.all()

    # Search term
    search_term = request.GET.get('search[value]', None)
    if search_term:
        base_query = base_query.filter(
            Q(punishment__icontains=search_term)
        )

    # Total records
    total_records = base_query.count()

    # Order by
    order_column = int(request.GET.get('order[0][column]', 0))
    order_dir = request.GET.get('order[0][dir]', 'asc')
    order_columns = ['punishment']
    if order_dir == 'asc':
        base_query = base_query.order_by(order_columns[order_column])
    else:
        base_query = base_query.order_by(f'-{order_columns[order_column]}')

    # Page and page length
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 5))
    end = start + length

    # Get the data for the current page
    filtered_data = base_query[start:end]

    # Construct the JSON response
    response = {
        'draw': int(request.GET.get('draw', 0)),
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': [
            {
                'id': item.id,
                'punishment': item.punishment,
                'actions': f'<button type="button" onclick="addPunishment({item.id}, \'{item.punishment}\')" class="btn btn-sm btn-info mr-auto">Use</button>'
            } for item in filtered_data
        ]
    }

    return JsonResponse(response)

def place_of_omission(request):
    """AJAX request to retrieve the personnel's data."""
    # Define the base queryset
    base_query = PlaceOfOmission.objects.all()

    # Search term
    search_term = request.GET.get('search[value]', None)
    if search_term:
        base_query = base_query.filter(
            Q(place__icontains=search_term) |
            Q(date__icontains=search_term)
        )

    # Total records
    total_records = base_query.count()

    # Order by
    order_column = int(request.GET.get('order[0][column]', 0))
    order_dir = request.GET.get('order[0][dir]', 'asc')
    order_columns = ['place', 'date']
    if order_dir == 'asc':
        base_query = base_query.order_by(order_columns[order_column])
    else:
        base_query = base_query.order_by(f'-{order_columns[order_column]}')

    # Page and page length
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 5))
    end = start + length

    # Get the data for the current page
    filtered_data = base_query[start:end]

    # Construct the JSON response
    response = {
        'draw': int(request.GET.get('draw', 0)),
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': [
            {
                'place': item.place,
                'date': date_formatter2(item.date.strftime("%Y-%m-%dT%H:%M:%S%z")),
                'actions': f"""<button type="button" onclick="addDatePlaceOmission(
                        {item.id}, \'{date_formatter2(item.date.strftime("%Y-%m-%dT%H:%M:%S%z"))}\', 
                        \'{item.place}\')" class="btn btn-sm btn-info">Use</button>
                """
            } for item in filtered_data
        ]
    }

    return JsonResponse(response)


def get_submitted_offense_dt(request):
    """AJAX request to retrieve the personnel's data."""
    # Define the base queryset
    base_query = Offense.objects.all().order_by('entry_date')

    # Search term
    search_term = request.GET.get('search[value]', None)
    if search_term:
        base_query = base_query.filter(
            Q(personnel__afpsn__icontains=search_term) |
            Q(personnel__last_name__icontains=search_term) |
            Q(personnel__rank_id__icontains=search_term) |
            Q(offense__violation__icontains=search_term)
        )

    # Total records
    total_records = base_query.count()

    # Order by
    order_column = int(request.GET.get('order[0][column]', 0))
    order_dir = request.GET.get('order[0][dir]', 'asc')
    order_columns = ['personnel', 'offense', 'entry_date']
    if order_dir == 'asc':
        base_query = base_query.order_by(order_columns[order_column])
    else:
        base_query = base_query.order_by(f'-{order_columns[order_column]}')

    # Page and page length
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 5))
    end = start + length

    # Get the data for the current page
    filtered_data = base_query[start:end]

    # Construct the JSON response
    response = {
        'draw': int(request.GET.get('draw', 0)),
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': [
            {
                'personnel': item.personnel,
                'offense': item.offense,
                'entry_date': item.entry_date,
                'actions': f'<button type="button" onclick="refreshSubmittedViolationDt({item.id})" class="btn btn-sm btn-info mr-auto">View</button>'
            } for item in filtered_data
        ]
    }

    return JsonResponse(response)
