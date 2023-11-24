from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from django.db.models import Q
from book.models import (
    AFP_Personnel, OffenseLibrary, PlaceOfOmission,
    Offense, PunishmentLibrary, ImposedByWhom,
    Resolution
)
from django.http import JsonResponse
from book.utils.date_formatter import DateFormatter
from django.shortcuts import get_object_or_404
from django.urls import reverse

import json

# @login_required
def submission_page(request):
    context = {}
    return render(request, 'book/submission_page.html', context)


def all_violation_page(request):
    context = {}
    return render(request, 'book/all_violation_record.html', context)


def get_resolutions(request, pk):
    """Show list of resolution convert the table to list"""
    offense = get_object_or_404(Offense, id=pk)
    base_query = [offense.resolution]

    # Search term
    search_term = request.GET.get('search[value]', None)

    # Filter based on search term
    if search_term:
        base_query = [res for res in base_query if
                      any(str(value) for value in [res.date, res.decision_of_appeal, res.mitigation_re_remission,
                                                   res.intl_first_sergeant, res.initial_of_ep, res.remarks]
                          if value and search_term.lower() in str(value).lower())]

    # Total records
    total_records = len(base_query)

    # Order by
    order_column = request.GET.get('order[0][column]', 0)  # Default to 0 if not provided
    order_dir = request.GET.get('order[0][dir]', 'asc')
    order_columns = ['date', 'decision_of_appeal', 'mitigation_re_remission', 'intl_first_sergeant', 'initial_of_ep',
                     'remarks']

    # Make sure the order column index is within the range of order_columns
    order_column_index = int(order_column) if str(order_column).isdigit() and int(order_column) < len(
        order_columns) else 0
    order_field = order_columns[order_column_index]

    if order_dir == 'desc':
        base_query.reverse()

    # Page and page length
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 5))
    end = start + length

    # Get the data for the current page
    filtered_data = base_query[start:end]

    response = {
        'draw': int(request.GET.get('draw', 1)),
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': [
            {
                'date': DateFormatter(res.date.strftime("%Y-%m-%dT%H:%M:%S%z")).date_formatter2() if res else None,
                'decision_of_appeal': res.decision_of_appeal if res else None,
                'mitigation_re_remission': res.mitigation_re_remission if res else None,
                'intl_first_sergeant': res.intl_first_sergeant if res else None,
                'initial_of_ep': res.initial_of_ep if res else None,
                'remarks': res.remarks if res else None,
            } for res in filtered_data
        ]
    }

    return JsonResponse(response)


def submit_resolution(request, pk):
    success = False
    message = ''

    if request.method == 'POST':
        if not pk:
            message = 'Primary Key while submitting resolution is none!'
        else:
            try:
                data = json.loads(request.body)

                date = data.get('date')
                dec_appeal = data.get('dec_appeal')
                mitigation_remission = data.get('mitigation_remission')
                intl_first_sergeant = data.get('intl_first_sergeant')
                initial_of_ep = data.get('initial_of_ep')
                remarks = data.get('remarks')

                # Create an instance of the Resolution model
                resolution_instance = Resolution(
                    date=DateFormatter(date, '%Y-%m-%d %H:%M').format_date_make_aware(),
                    decision_of_appeal=dec_appeal,
                    mitigation_re_remission=mitigation_remission,
                    intl_first_sergeant=intl_first_sergeant,
                    initial_of_ep=initial_of_ep,
                    remarks=remarks
                )

                # Save the instance to the database
                resolution_instance.save()

                # Get the offense instance using the provided pk
                offense_instance = get_object_or_404(Offense, pk=pk)

                # Update the offense with the resolution
                offense_instance.resolution = resolution_instance

                # Save the offense instance to the database
                offense_instance.save()

                success = True
                message = 'Data processed and saved successfully'

            except json.JSONDecodeError:
                message = 'Invalid JSON data'
            except Exception as e:
                message = f'Error: {str(e)}'

    response = {
        'success': success,
        'message': message
    }

    return JsonResponse(response)


def view_violation_page(request, pk):
    """When user select one of the submitted case this will render"""
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

        violations = offense.offense.all()
        print(violations)
        context = {
            'pk': pk,
            'personnel_name': personnel_name,
            'article_of_war': violations,
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
            Q(authori=search_term) |
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
                'entry_date': DateFormatter(item.entry_date.strftime("%Y-%m-%dT%H:%M:%S%z")).date_formatter2(),
                'actions': f'<button type="button" onclick="window.location.href=\'{reverse("view_violation_page", args=[item.id])}\'" class="btn btn-sm btn-info mr-auto">View</button>',
            } for item in filtered_data
        ],
        'length': length
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

            omission_date = DateFormatter(omission_date, '%Y-%m-%d %H:%M:%S').format_date_make_aware()

            # Fetch related objects using provided IDs
            violation_obj = get_object_or_404(OffenseLibrary, id=violation[0])

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
            aware_date_notice = DateFormatter(date_notice, '%Y-%m-%d %H:%M').format_date_make_aware()

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
                'date': DateFormatter(item.date.strftime("%Y-%m-%dT%H:%M:%S%z")).date_formatter2(),
                'actions': f"""<button type="button" onclick="addDatePlaceOmission(
                        {item.id}, \'{DateFormatter(item.date.strftime("%Y-%m-%dT%H:%M:%S%z")).date_formatter2()}\', 
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
