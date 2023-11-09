function initializeResolutionsDt() {
    var pk = $('#resolutionDT').data('pk');
    console.log('View Offense PKey:', pk);  // Output the primary key to the console

    var resolutionsTable = $('#resolutionDT').DataTable({
        responsive: true,
        serverSide: true,
        processing: true,
        ajax: {
            url: '/get-resolutions/' + pk + '/',
            type: 'GET',
        },
        columns: [
            { data: 'decision_of_appeal' },
            { data: 'mitigation_re_remission' },
            { data: 'remarks' },
            { data: 'date' },
            { data: 'intl_first_sergeant' },
            { data: 'initial_of_ep' }
        ]
    });

    // Function to refresh the DataTable
    function fetchResolutions() {
        resolutionsTable.ajax.reload();
    }

    // Trigger DataTable refresh when the button is clicked
    $('#refreshResolutions').on('click', function () {
        event.preventDefault();
        fetchResolutions();
    });
}
