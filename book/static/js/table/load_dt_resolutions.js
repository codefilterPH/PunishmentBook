function initializeResolutionsDt() {
    var pk = $('#resolutionDT').data('pk');
    if (pk) { console.log('View Offense PKey:', pk); }

    var resolutionsTable = $('#resolutionDT').DataTable({
        responsive: true,
        serverSide: true,
        processing: true,
        ajax: {
            url: '/get-resolutions/' + pk + '/',
            type: 'GET',
        },
        columns: [
            { data: 'date' },
            { data: 'decision_of_appeal' },
            { data: 'mitigation_re_remission' },
            { data: 'intl_first_sergeant' },
            { data: 'initial_of_ep' },
            { data: 'remarks' }
        ],

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
