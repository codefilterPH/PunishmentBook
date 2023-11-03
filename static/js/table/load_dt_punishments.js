function initializePunishmentDt() {

    var punishmentTable = $('#punishmentTable').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: '/get-punishments-dt/',
            type: 'GET',
        },
        columns: [
            { data: 'punishment' },
            { data: 'actions' }
        ]
    });

    // Function to refresh the DataTable
    function fetchPunishment() {
        punishmentTable.ajax.reload();
    }

    // Trigger DataTable refresh when the button is clicked
    $('#refreshPunishment').on('click', function () {
        event.preventDefault();
        fetchPunishment();
    });
}
