function submitDeleteForm(event, form) {
    event.preventDefault();

    var form = event.target;
    var url = form.action;

    var xhr = new XMLHttpRequest();
    xhr.open("DELETE", url, true);
    xhr.onload = function() {
        handleResponse(xhr);
    };

    xhr.send();
}

function submitEditForm(event, form, methodOverride) {
    event.preventDefault();

    var url = form.action;

    var xhr = new XMLHttpRequest();
    xhr.open(methodOverride, url, true);
    xhr.setRequestHeader("X-HTTP-Method-Override", methodOverride);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        handleResponse(xhr);
    };

    var formData = new FormData(form);
    var params = new URLSearchParams(formData).toString();
    xhr.send(params);

    return false;
}

function handleResponse(xhr) {
    if (xhr.status === 200) {
        console.log('Replacing current page with html response.')
        var responseHtml = xhr.responseText;
        document.open();
        document.write(responseHtml);
        document.close();
    } else if (xhr.status === 204) {
        window.location.reload();
    } else if (xhr.status === 303 || xhr.status === 302 || xhr.status === 301) {
        console.log('Following redirect to', xhr.getResponseHeader("Location"));
    } else {
        console.log("Request failed with status:", xhr.status);
    }
}

function addSubmitListener() {
    document.addEventListener("submit", function(event) {
        var form = event.target;
        var methodOverride = form.querySelector('input[name="_method"]').value.toUpperCase();

        if (methodOverride === "PUT" || methodOverride === "PATCH") {
            return submitEditForm(event, form, methodOverride);
        } else if(methodOverride === "DELETE") {
            return submitDeleteForm(event, form);
        } else {
            return true;
        }
    });
}

window.onload = function() {
    addSubmitListener();
};