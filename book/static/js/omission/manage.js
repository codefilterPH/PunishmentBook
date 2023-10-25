function formatReceivedDate(inputDate) {
    try {
        console.log('RECEIVED DATE: ' + inputDate + '\n\n');

        // Parse the input date string to a Date object
        const inputDateObj = new Date(inputDate);

        // Format the Date object as "YYYY-MM-dd"
        const formattedDate = inputDateObj.toISOString().split('T')[0];

        return formattedDate;
    } catch (error) {
        return 'Error: ' + error;
    }
}


function addDatePlaceOmission(id, entry_date, place) {
    console.log('RECEIVED ID: ' + id);
    console.log('RECEIVED DATE: ' +  formatReceivedDate(entry_date));
    console.log('RECEIVED PLACE: ' + place);
    // Set the value and ID of the "dateOmission" input field
    $('#dateOmission').val(entry_date).attr('data-id', id);
    $('#placeOmission').val(place).attr('data-id', id);
}
