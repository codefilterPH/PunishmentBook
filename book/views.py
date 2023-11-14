from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from django.db.models import Q
from book.models import (
    AFP_Personnel, OffenseLibrary, PlaceOfOmission, Offense, PunishmentLibrary, ImposedByWhom
)
from django.http import JsonResponse
from book.utils.date_formatter import date_formatter2
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime
from django.urls import reverse

import json
import pytz


# @login_required
def submission_page(request):
    context = {}
    return render(request, 'book/submission_page.html', context)


def all_violation_page(request):
    context = {}
    return render(request, 'book/all_violation_record.html', context)

def get_resolutions(request, pk):
    offense = get_object_or_404(Offense, id=pk)
    base_query = offense.resolution.all()
    # Search term
    search_term = request.GET.get('search[value]', None)
    if search_term:
        base_query = base_query.filter(
            Q(decision_of_appeal__icontains=search_term) |
            Q(mitigation_re_remission__icontains=search_term) |
            Q(remarks__icontains=search_term) |
            Q(date__icontains=search_term) |
            Q(intl_first_sergeant__icontains=search_term) |
            Q(initial_of_ep__icontains=search_term)
        )

        # Total records
    total_records = base_query.count()

    # Order by
    order_column = request.GET.get('order[0][column]', 'date')  # Default to 'date' if not provided
    order_dir = request.GET.get('order[0][dir]', 'asc')
    order_columns = ['date', 'decision_of_appeal']  # Add the fields you want to be able to sort by

    # Make sure the order column index is within the range of order_columns
    order_column_index = int(order_column) if order_column.isdigit() and int(order_column) < len(order_columns) else 0
    order_field = order_columns[order_column_index]

    if order_dir == 'asc':
        base_query = base_query.order_by(order_field)
    else:
        base_query = base_query.order_by(f'-{order_field}')

    # Page and page length
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 5))
    end = start + length

    # Get the data for the current page
    filtered_data = base_query[start:end]

    # Construct the JSON response
    response = {
        'draw': int(request.GET.get('draw', 1)),  # Default to 1 if not provided
        'recordsTotal': total_records,
        'recordsFiltered': total_records,  # Assuming no additional filtering is done beyond the search term
        'data': [
            {
                'decision_of_appeal': resolution.decision_of_appeal,
                'mitigation_re_remission': resolution.mitigation_re_remission,
                'remarks': resolution.remarks,
                'date': date_formatter2(resolution.date.strftime("%Y-%m-%dT%H:%M:%S%z")),
                'intl_first_sergeant': resolution.intl_first_sergeant,
                'initial_of_ep': resolution.initial_of_ep,
            } for resolution in filtered_data
        ]
    }

    return JsonResponse(response)

def view_violation_page(request, pk):
    print(f'Primary Key: {pk}')

    try:
        # Use get_object_or_404 to retrieve the offense or raise a 404 error if it doesn't exist.
        offense = get_object_or_404(Offense, id=pk)

        # Access the related personnel using the 'personnel' ForeignKey field.
        personnel = offense.personnel
        rank = personnel.rank_id
        first = personnel.first_name
        last = personnel.last_name
        middle = personnel.middle_name
        afpsn = personnel.afpsn

        # Now you can access the name of the personnel.
        personnel_name = "{} {} {} {} {}".format(rank, first, middle, last, afpsn)
        print("Personnel Name:", personnel_name)

        omission = offense.place
        date_accused = offense.entry_date

        context = {
            'pk': pk,
            'personnel_name': personnel_name,
            'violations': offense.offense.all(),
            'punishments': offense.punishments.all(),
            'date_of_omission': omission.date,
            'place_of_omission': omission.place,
            'imposed_by_whom': offense.imposer.all(),
            'date_accused': date_accused
        }
    except Offense.DoesNotExist:
        # Handle the case where the offense with the given ID does not exist.
        context = {
            'error_message': f"Offense with ID {pk} does not exist.",
        }

    return render(request, 'book/view_violation_page.html', context)

def submitted_offense_dt(request):
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

    # Need Search by multiple fields
    # Modal in every row with click functionality

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
                'personnel': str(item.personnel),
                'offense': ', '.join([str(violation) for violation in item.offense.all()]),
                'entry_date': date_formatter2(item.entry_date.strftime("%Y-%m-%dT%H:%M:%S%z")),
                'actions': f'<button type="button" onclick="window.location.href=\'{reverse("view_violation_page", args=[item.id])}\'" class="btn btn-sm btn-info mr-auto">View</button>',
                # 'actions': f'<button type="button" onclick="" class="btn btn-sm btn-info mr-auto">View</button>'

            } for item in filtered_data
        ]
    }

    return JsonResponse(response)


# @login_required
def submit_function(request):
    success = False
    message = ''
    if request.method == 'POST':
        data = json.loads(request.body)
        if data:
            personnel_list = data.get('personnel')
            violation = data.get('violation')
            omission_date = data.get('omission_date')
            omission_place = data.get('omission_place')
            punishment = data.get('punishment')
            imposer = data.get('imposer')
            date_notice = data.get('date_notice')

            # Convert the string to a timezone-aware datetime object
            naive_datetime = datetime.strptime(omission_date, '%Y-%m-%d %H:%M:%S')
            omission_date = timezone.make_aware(naive_datetime, timezone=pytz.UTC)

            # Fetch related objects using provided IDs
            violation_obj = get_object_or_404(OffenseLibrary,
                                              id=violation[0])  # Assuming only one violation is selected

            # Get or create a PlaceOfOmission instance
            place_obj, created = PlaceOfOmission.objects.get_or_create(
                place=omission_place,
                date=omission_date,
                defaults={
                    'place': omission_place,
                    'date': omission_date
                }
            )

            # Convert the date_notice string to a timezone-aware datetime object
            naive_datetime_notice = datetime.strptime(date_notice, '%Y-%m-%d %H:%M')
            aware_date_notice = timezone.make_aware(naive_datetime_notice, timezone=pytz.UTC)

            for personnel_id in personnel_list:
                personnel_obj = get_object_or_404(AFP_Personnel, id=personnel_id)

                # Create a new Offense instance
                # Create the Offense instance without the many-to-many fields
                offense_instance = Offense(
                    personnel=personnel_obj,
                    place=place_obj,
                    entry_date=aware_date_notice
                )
                offense_instance.save()

                # Set the many-to-many relationships
                offense_instance.offense.set([violation_obj])

                punishment_objs = PunishmentLibrary.objects.filter(id__in=punishment)
                offense_instance.punishments.set(punishment_objs)

                imposer_objs = ImposedByWhom.objects.filter(id__in=imposer)
                offense_instance.imposer.set(imposer_objs)

            success = True
            message = 'Data processed successfully'

    response = {
        'success': success,
        'message': message
    }

    return JsonResponse(response)


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


def get_violations_dt(request):
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
                'actions': f'<button type="button" onclick="addViolations({item.id}, \'{item.violation}\')" class="btn btn-sm btn-info mr-auto">Use</button>'
            } for item in filtered_data
        ]
    }

    return JsonResponse(response)


def get_punishments_dt(request):
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


def get_imposed_by_whom_dt(request):
    """AJAX request to retrieve the personnel's data."""
    # Define the base queryset
    base_query = ImposedByWhom.objects.all()

    # Search term
    search_term = request.GET.get('search[value]', None)
    if search_term:
        base_query = base_query.filter(
            Q(name__icontains=search_term)
        )

    # Total records
    total_records = base_query.count()

    # Order by
    order_column = int(request.GET.get('order[0][column]', 0))
    order_dir = request.GET.get('order[0][dir]', 'asc')
    order_columns = ['name']
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
                'name': item.name,
                'actions': f'<button type="button" onclick="imposedByWhom({item.id}, \'{item.name}\')" class="btn btn-sm btn-info mr-auto">Select</button>'
            } for item in filtered_data
        ]
    }

    return JsonResponse(response)
