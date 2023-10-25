function get_from_list_box(need) {
    // Get the selected options from the "Selected Personnel" <select> element
    var selectedOptions;
    if (need == 'personnel') {
        var selectedOptions = $('#personnel option:selected');
    }
    else if (need == 'punishment') {
        var selectedOptions = $('#punishmentList option:selected');
    }

    // Create an array to store the selected option values
    var selectedValues = [];

    // Iterate through the selected options and add their values to the array
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


$(document).ready(function() {
    var form = $('#submitForm');
    var submitButton = $('#submitOffenseBtn');

    submitButton.click(function(event) {
        event.preventDefault();

        var personnel = get_from_list_box('personnel');
        console.log('Selected Personnel IDs: ', personnel);

        var omissionValue = datePlaceOmission();
        console.log('Selected Date of Omission: ' + omissionValue.date_of_omission);
        console.log('Selected Place of Omission: ' + omissionValue.place_of_omission);

        var punishment = get_from_list_box('punishment');
        console.log('Selected Punishment\'s Value: ', punishment);

        var date_notice = dateOfNotice();
        console.log('Selected Date of Notice Value: ', date_notice);

        // Continue with your form submission logic
        // form.submit(); // Uncomment this line to submit the form
    });
});
