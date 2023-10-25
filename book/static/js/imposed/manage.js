
function imposedByWhom(id, name) {
    console.log('RECEIVED ID: ' + id);
    console.log('RECEIVED NAME: ' +  name);

    // Get the <select> element
    var selectElement = $('#imposedByWhomList');

    // Check if the personnel is already selected
    if (selectElement.find('option[value="' + id + '"]').length === 0) {
        // Create a new <option> element
        var option = $('<option>', {
            value: id,
            text: name
        });
           // Set the 'selected' attribute for the newly created option
        option.prop('selected', true);

        // Append the new option to the <select> element
        selectElement.append(option);
    }
}