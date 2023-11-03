function get_from_list_box(need) {
    // Get the selected options from the "Selected Personnel" <select> element
    var selectedOptions;
    if (need == 'personnel') {
        var selectedOptions = $('#personnel option:selected');
    }
    else if (need == 'imposer') {
        var selectedOptions = $('#imposedByWhomList option:selected');
    }
    else if (need == 'violation') {
        var selectedOptions = $('#violationList option:selected');
    }
    else if (need == 'punishment') {
        var selectedOptions = $('#punishmentList option:selected');
    }

    var selectedValues = [];
    selectedOptions.each(function() {
        selectedValues.push($(this).val());
    });

    return selectedValues;
}

function datePlaceOmission() {
    // Get the values of the "dateOmission" and "placeOmission" <input> elements
    var dateOmission = $('#dateOmission').val();
    var placeOmission = $('#placeOmission').val();

    var dataValue = {
        'date_of_omission': dateOmission,
        'place_of_omission': placeOmission
    };

    return dataValue;
}

function dateOfNotice() {
    // Get the values of the "dateOmission" and "placeOmission" <input> elements
    return $('#dateOfNotice').val();
}


function verify_data(data) {
    for (var key in data) {
        if (data.hasOwnProperty(key)) {
            var value = data[key];

            if (Array.isArray(value) && value.length === 0) {
                error_message('Please fill in all the fields.').then(() => {
                    console.log("User acknowledged the error.");
                });
                return false;
            } else if (typeof value === 'object') {
                for (var subKey in value) {
                    if (!value[subKey] || value[subKey].length === 0) {
                        error_message('Please fill in all the fields.').then(() => {
                            console.log("User acknowledged the error.");
                        });
                        return false;
                    }
                }
            } else if (!value || value.length === 0) {
                error_message('Please fill in all the fields.').then(() => {
                    console.log("User acknowledged the error.");
                });
                return false;
            }
        }
    }
    return true;
}

$(document).ready(function() {
    var form = $('#submitForm');
    var submitButton = $('#submitOffenseBtn');

    submitButton.click(function(event) {
        event.preventDefault();

        var personnel = get_from_list_box('personnel');
        console.log('Selected Personnel IDs: ', personnel);

        var violation = get_from_list_box('violation');
        console.log('Selected Violation\'s Value: ', violation);

        var omissionValue = datePlaceOmission();
        console.log('Selected Date of Omission: ' + omissionValue.date_of_omission);
        console.log('Selected Place of Omission: ' + omissionValue.place_of_omission);

        var punishment = get_from_list_box('punishment');
        console.log('Selected Punishment\'s Value: ', punishment);

        var imposer = get_from_list_box('imposer');
        console.log('Selected Imposed by Whom\'s Value: ', imposer);

        var date_notice = dateOfNotice();
        console.log('Selected Date of Notice Value: ', date_notice);

        // COMBINE ALL VARIABLE AS ONE

        var data = {
            personnel: personnel,
            violation: violation,
            omission_date: omissionValue.date_of_omission,
            omission_place: omissionValue.place_of_omission,
            punishment: punishment,
            imposer: imposer,
            date_notice: date_notice
        };

        console.log('Data:', data);
        if (!verify_data(data)) {
            return;
        }

        var csrfToken = $('meta[name="csrf-token"]').attr('content');

        // Send data to Django view using AJAX
        $.ajax({
            url: form.attr('action'),  // get the URL from the form's action attribute
            type: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function(response) {
                // Handle success - maybe redirect or show a success message
                console.log('SUCCESS: ' + response.success);
                console.log('MESSAGE: ' + response.message);
                success_message(response.message);
                //window.location.href = '/personnel-violation-page/';  // example redirect
            },
            error: function(error) {
                // Handle error - maybe show an error message
                console.error(error);
                error_message('There was an error processing your request.');
            }
        });

    });
});
