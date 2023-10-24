$(document).ready(function () {
    // Define the DataTable
    var personnelTable = $('#showPersonnel').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: '/get-personnel/',
            type: 'GET',
            // You can include data like ref_id here if needed
        },
        columns: [
            { data: 'rank_id' },
            { data: 'first_name' },
            { data: 'middle_name' },
            { data: 'last_name' },
            { data: 'afpsn' },
            { data: 'actions' },  // If you have actions column
        ]
    });

    // Function to refresh the DataTable
    function fetchPersonnel() {
        personnelTable.ajax.reload();
    }

    // Trigger DataTable refresh when the button is clicked
    $('#refreshDataTable').on('click', function () {
        fetchPersonnel();
    });
});
