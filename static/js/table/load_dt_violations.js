function initializeViolationsDT() {

    var violationsTable = $('#violationsTable').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: '/get-violations-dt/',
            type: 'GET',
        },
        columns: [
            { data: 'violation' },
            { data: 'actions' }
        ]
    });

    // Function to refresh the DataTable
    function fetchViolations() {
        violationsTable.ajax.reload();
    }

    // Trigger DataTable refresh when the button is clicked
    $('#refreshViolations').on('click', function () {
        event.preventDefault();
        fetchViolations();
    });
}
