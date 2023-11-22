

$(document).ready(function() {
    var form = $('#newResolutionForm');
    var btnSubmitResolution = $('#btnSubmitResolution');

    btnSubmitResolution.click(function(event) {
        event.preventDefault();
        var dateResolution = $('#dateResolution').val();
        var decisionOfAppeal = $('#decisionOfAppeal').val();
        var mitigationRemission = $('#mitigationRemission').val();
        var intlFirstSergeant = $('#intlFirstSergeant').val();
        var initialOfEp = $('#initialOfEp').val();
        var remarks = $('#remarks').val();

        var data = {
            date: dateResolution,
            dec_appeal: decisionOfAppeal,
            mitigation_remission: mitigationRemission,
            intl_first_sergeant: intlFirstSergeant,
            initial_of_ep: initialOfEp,
            remarks: remarks,
        };

        console.log('Data:', data);

        var csrfToken = $('meta[name="csrf-token"]').attr('content');

        // Send data to Django view using AJAX
        $.ajax({
            url: form.attr('action'),  // get the URL from the form's action attribute
            type: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function(response) {
                // Handle success - maybe redirect or show a success message
                console.log('SUCCESS: ' + response.success);
                console.log('MESSAGE: ' + response.message);
                success_message(response.message);
                $('#closeModalViewViolation').click();

                $('#dateResolution').val('');
                $('#decisionOfAppeal').val('');
                $('#mitigationRemission').val('');
                $('#intlFirstSergeant').val('');
                $('#initialOfEp').val('');
                $('#remarks').val('');

                $('#refreshResolutions').click();
            },
            error: function(error) {
                // Handle error - maybe show an error message
                console.error(error);
                error_message('There was an error processing your request.');
            }
        });

    });
});
