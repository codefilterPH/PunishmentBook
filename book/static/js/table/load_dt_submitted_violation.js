
/**
 * Initializes the DataTable for submitted violations.
 *
 * @param {Object} params - Parameters for customization.
 *   @property {string} params.excelUrl - The URL of the Excel template file.
 */
function initSubmittedViolationsDT(params) {
    var submittedViolation = $('#submittedViolationDt').DataTable({
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excel',
                text: 'Export to Excel',
//                action: function () {
//                    var templatePath = params.excelUrl;
//                    var data = submittedViolation.ajax.json().data;
//
//                    customizeWorksheet(XLSX, templatePath, data);
//                }
            },
            {
                extend: 'csv',
                text: 'Export to CSV',
            },
            {
                extend: 'copy',
                text: 'Copy to Clipboard',
            },
            {
                extend: 'pdf',
                text: 'Export as PDF',
            },
            'print',
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
