// Function to add personnel to the <select> element
function addViolations(
        id, violation
    ) {

    console.log('ID:' + id);
    console.log('VIOLATION:' + violation)

    // Get the <select> element
    var selectElement = $('#violationList');

    // Check if the personnel is already selected
    if (selectElement.find('option[value="' + id + '"]').length === 0) {
        // Create a new <option> element
        var option = $('<option>', {
            value: id,
            text: violation
        });

        // Append the new option to the <select> element
        selectElement.append(option);
    }
}
