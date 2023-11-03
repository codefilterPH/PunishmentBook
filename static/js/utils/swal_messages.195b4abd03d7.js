function error_message(message) {
    return Swal.fire({
        title: 'Error',
        text: message,
        icon: 'error',
        confirmButtonText: 'Okay'
    });
}

function success_message(message) {
    return Swal.fire({
        title: 'Success',
        text: message,
        icon: 'success',
        confirmButtonText: 'Okay'
    });
}
