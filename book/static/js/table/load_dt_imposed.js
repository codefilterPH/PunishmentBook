function initializeImposedDt() {

    var imposerTable = $('#imposerTable').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: '/get-imposed-by-whom-dt/',
            type: 'GET',
        },
        columns: [
            { data: 'name' },
            { data: 'actions' }
        ]
    });

    // Function to refresh the DataTable
    function fetchImposer() {
        imposerTable.ajax.reload();
    }

    // Trigger DataTable refresh when the button is clicked
    $('#refreshImposerRecords').on('click', function () {
        event.preventDefault();
        fetchImposer();
    });
}
