
function initSubmittedViolationsDT() {
    var submittedViolation = $('#submittedViolationDt').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print',
        ],
        serverSide: true,
        processing: true,
        ajax: {
            url: '/submitted-offense-dt/',
            type: 'GET',
        },
        columns: [
            { data: 'personnel' },
            { data: 'offense' },
            { data: 'entry_date' },
            { data: 'actions' }
        ],
        lengthMenu: [10, 25, 50, 100],
    });

    // Function to refresh the DataTable
    function fetchSubmittedOffense() {
        submittedViolation.ajax.reload();
    }

    // Trigger DataTable refresh when the button is clicked
    $('#btnRefresh').on('click', function () {
        fetchSubmittedOffense();
        console.log('clicked submitted violations');
    });
}
