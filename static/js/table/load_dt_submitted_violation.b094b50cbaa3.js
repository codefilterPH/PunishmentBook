
function initSubmittedViolationsDT() {
    console.log('AMEN');
    var submittedViolation = $('#submittedViolationDt').DataTable({
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
        ]
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
