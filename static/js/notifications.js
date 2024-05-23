const baseUrl = "http://127.0.0.1:8000";

function updateNotifications() {
    let requestUrl = new URL("ajax/load-notifications/", baseUrl);
    $.ajax({
        url: requestUrl,
        type:'json',
        method:'GET',
        success: function (data) {
            $("#note_list").html(data);
        }
    });
};

function readNotification(element, pk) {
    element.classList.add('text-secondary');
    let requestUrl = new URL("notifications/read/" + pk + "/", baseUrl);
    $.ajax({
            url: requestUrl,
            type:'json',
            method:'GET'
    });
};

function deleteNotification(element, pk) {
    const csrftoken = getCookie('csrftoken');
    element.parentNode.parentNode.removeChild(element.parentNode);
    let requestUrl = new URL("notifications/delete/" + pk + "/", baseUrl);
    $.ajax({
            url: requestUrl,
            type:'json',
            method:'POST',
            headers: {
                'X-CSRFToken': csrftoken // Установка CSRF-токена в заголовок
            },
    });
};

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = jQuery.trim(cookies[i]);
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break; // Выходим, как только найдём нужное cookie
            }
        }
    }
    return cookieValue;
}