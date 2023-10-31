function initializeOmissionDataTable() {
    // # placeOmissionTable is the id of the table
    var omissionTable = $('#placeOmissionTable').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: '/get-place-omission/',
            type: 'GET',
        },
        columns: [
            { data: 'place' },
            { data: 'date' },
            { data: 'actions' }
        ]

        // this columns are auto assigned to table tbody as rows
    });

    // Function to refresh the DataTable
    function fetchPlaceOmission() {
        omissionTable.ajax.reload();
    }

    // Trigger DataTable refresh when the button is clicked
    // # refreshOmission is just a load button
    $('#refreshOmission').on('click', function () {
        event.preventDefault();
        fetchPlaceOmission();
    });
}
