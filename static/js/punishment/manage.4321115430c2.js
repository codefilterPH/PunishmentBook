// Function to add punishment to the <select> element
function addPunishment(
        id, punishment
    ) {

    console.log('ID: ' + id);
    console.log('PUNISHMENT: ' + punishment)

    // Get the <select> element
    var selectElement = $('#punishmentList');

    // Check if the personnel is already selected
    if (selectElement.find('option[value="' + id + '"]').length === 0) {
        // Create a new <option> element
        var option = $('<option>', {
            value: id,
            text: punishment
        });
           // Set the 'selected' attribute for the newly created option
        option.prop('selected', true);

        // Append the new option to the <select> element
        selectElement.append(option);
    }
}
