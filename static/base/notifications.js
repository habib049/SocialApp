window.addEventListener('load', (event) => {

    //adding event listeners to add friend option
    let addFriendButtons = document.getElementsByClassName('add-friend');
    for (let i = 0; i < addFriendButtons.length; i++) {
        addFriendButtons[i].addEventListener('click', sendFriendRequest)
    }

    function sendFriendRequest(e) {
        e.preventDefault();
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            type: 'POST',
            data: {
                'userId': this.id.toString().split('-')[1]
            },

            url: '/friend/send-request',
            dataType: 'json',
            success: function (data) {
                console.log(data);
            }
        });
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    //websocket work for realtime notification

    let friendRequestNotificationSocket = new ReconnectingWebSocket(
        //providing a path
        'ws://' + window.location.host + '/ws/friend-request-notification/'
    )

    friendRequestNotificationSocket.onopen = (e) => {
        alert('connection open')
    }

    friendRequestNotificationSocket.onmessage = (e) => {
        console.log(e)
        alert("message received")
    }

    friendRequestNotificationSocket.onmessageerror = (e) => {
        alert("message error")
    }

    friendRequestNotificationSocket.onclose = (e) => {
        alert('connection close')
    }

})