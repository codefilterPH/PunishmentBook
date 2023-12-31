// Function to add personnel to the <select> element
function addPersonnel(
        personnelId, rank_id, first_name, middle_name, last_name, afpsn
    ) {
    // Get the <select> element
    var selectElement = $('#personnel');

    console.log('PERSONNEL\'S ID: ' + personnelId);

    // Check if the personnel is already selected
    if (selectElement.find('option[value="' + personnelId + '"]').length === 0) {
        // Create a new <option> element
        var option = $('<option>', {
            value: personnelId,
            text: rank_id + " " + first_name + " " + middle_name + " " + last_name + " " + afpsn
        });
        // Set the 'selected' attribute for the newly created option
        option.prop('selected', true);

        // Append the new option to the <select> element
        selectElement.append(option);
    }
}
