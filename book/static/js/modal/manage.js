// Close modal functionality
    function closeModal() {
        $('.modal').modal('hide');
    }

    // Submit form and close modal on success
    $('#newResolutionForm').on('submit', function(e) {
        e.preventDefault();
        var formData = $(this).serialize(); // Serialize the form data
         closeModal();
//        // Perform AJAX request (you need to replace 'your_submit_resolution_url_name' with the actual URL)
//        $.ajax({
//            url: "{% url 'your_submit_resolution_url_name' %}",
//            type: 'POST',
//            data: formData,
//            success: function(response) {
//                // Handle success
//                console.log('Form submitted successfully');
//                closeModal(); // Close the modal if the submission is successful
//                $('#resolutionDT').DataTable().ajax.reload();
//            },
//            error: function(error) {
//                // Handle error
//                console.log('An error occurred');
//            }
//        });
    });

   $('#hideModalViewViolation').on('click', function(e) {
        e.preventDefault(); // Prevent default action if it's a submit button or a link
        closeModal(); // Call the closeModal function
   });

   $('#closeModalViewViolation').on('click', function(e) {
        e.preventDefault(); // Prevent default action if it's a submit button or a link
        closeModal(); // Call the closeModal function
    });
