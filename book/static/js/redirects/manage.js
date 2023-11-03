// LOAD THE VIEW PAGE

function redirectToView(id) {
    if (id) {
        // Generate the URL using the view name and include the 'id' parameter
        var url = "{% url 'view_offense_page' id=id %}";
        // Perform the redirection
        window.location.href = url;
    } else {
        console.error('ID is empty or undefined.');
    }
}
