function sendAjax(url, data, callback, method = "POST") {
    fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
            "X-Requested-With": "XMLHttpRequest"
        },
        body: data ? JSON.stringify(data) : null
    })
    .then(response => {
        if (!response.ok) throw new Error("Network error");
        return response.json();
    })
    .then(callback)
    .catch(error => console.error("AJAX error:", error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
