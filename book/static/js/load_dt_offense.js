function initializeOffenseDataTable() {

    var showOffenseTable = $('#showOffenseTable').DataTable({
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
        showOffenseTable.ajax.reload();
    }

    // Trigger DataTable refresh when the button is clicked
    $('#refreshOffenseRecords').on('click', function () {
        fetchOffense();
    });
}
