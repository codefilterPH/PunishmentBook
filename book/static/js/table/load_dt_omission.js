function initializeOmissionDataTable() {
    console.log('INITIALIZE OMISSION DATATABLE');
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
    });

    // Function to refresh the DataTable
    function fetchPlaceOmission() {
        omissionTable.ajax.reload();
    }

    // Trigger DataTable refresh when the button is clicked
    $('#refreshOmission').on('click', function () {
        event.preventDefault();
        fetchPlaceOmission();
    });
}
