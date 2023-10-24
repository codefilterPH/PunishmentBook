function initializeOffenseDataTable() {

    var offenseTable = $('#offenseTable').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: '/get-offense/',
            type: 'GET',
        },
        columns: [
            { data: 'violation' },
            { data: 'actions' }
        ]
    });

    // Function to refresh the DataTable
    function fetchOffense() {
        offenseTable.ajax.reload();
    }

    // Trigger DataTable refresh when the button is clicked
    $('#refreshViolations').on('click', function () {
        fetchOffense();
    });
}
