function initializeSubmittedOffenseDT() {

    var submittedViolation = $('#submittedViolationDt').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: '/submitted-offense-dt/',
            type: 'GET',
        },
        columns: [
            { data: 'place' },
            { data: 'date' },
            { data: 'actions' }
        ]
    });

    // Function to refresh the DataTable
    function fetchSubmittedOffense() {
        submittedViolation.ajax.reload();
    }

    // Trigger DataTable refresh when the button is clicked
    $('#refreshSubmittedViolationDt').on('click', function () {
        fetchSubmittedOffense();
    });
}
