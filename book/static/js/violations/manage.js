// Function to add personnel to the <select> element
function addViolations(id, violation) {
    // Get the <select> element
    console.log('ID:' + id);
    console.log('VIOLATION:' + violation);

    var selectElement = $('#violationList');

    // Check if the personnel is already selected
    if (selectElement.find('option[value="' + id + '"]').length === 0) {
        // Create a new <option> element
        var option = $('<option>', {
            value: id,
            text: violation,
            selected: true
        });
        // Set the 'selected' attribute for the newly created option
        option.prop('selected', true);

        // Append the new option to the <select> element
        selectElement.append(option);
    }
}
