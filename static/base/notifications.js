window.addEventListener('load', (event) => {

    //adding event listeners to add friend option
    let addFriendButtons = document.getElementsByClassName('add-friend');
    for (let i = 0; i < addFriendButtons.length; i++) {
        addFriendButtons[i].addEventListener('click', sendFriendRequest)
    }

    //adding event listeners to accept friend request
    addEventListenersAcceptFriendRequest();

    function addEventListenersAcceptFriendRequest() {
        let acceptFriendButtons = document.getElementsByClassName('confirm-request');
        for (let i = 0; i < acceptFriendButtons.length; i++) {
            acceptFriendButtons[i].addEventListener('click', acceptFriendRequest)
        }
    }


    function sendFriendRequest(e) {
        alert("in function")
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

            url: '/friend/send-friend-request',
            dataType: 'json',
            success: function (data) {
                console.log(data);
            }
        });
    }

    function acceptFriendRequest(e) {
        alert("in function")
        e.preventDefault();
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            type: 'POST',
            data: {
                'username': this.id.toString().split('-')[1]
            },

            url: '/friend/accept-friend-request',
            dataType: 'json',
            success: function (data) {
                console.log(data);
            }
        });
    }


    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = jQuery.trim(cookies[i]);
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
        // alert('connection open')
    }

    friendRequestNotificationSocket.onmessage = (e) => {
        let data = JSON.parse(e.data);
        setNotification(data.sender, data.receiver, data.message, data.imageUrl, data.type)
    }

    friendRequestNotificationSocket.onmessageerror = (e) => {
        // alert("message error")
    }

    friendRequestNotificationSocket.onclose = (e) => {
        // alert('connection close')
    }
    let receiverId = "";

    function setNotification(sender, receiver, message, imageUrl, type) {
        receiverId = "user-" + receiver;
        document.getElementById(receiverId).innerHTML = "<div class=\"alert alert-success alert-dismissable\" id=\"user-notification\">\n" +
            "      <div class='notification-section'><div class=\"user-image\">\n" +
            "                    <img src=\"" + imageUrl + "\" alt=\"\">\n" +
            "                </div>\n" +
            "                <div class=\"user-info-section\">\n" +
            "                    <div class=\"username\">\n" +
            "                        <h6>" + sender + "</h6>\n" +
            "                    </div>\n" +
            "                    <div class=\"message\">\n" +
            "                        <h6>" + message + "</h6>\n" +
            "                    </div>\n" +
            "                </div></div>   \n" +
            "                <div class=\"close-section\" id=\"" + receiver + "-notification-close-button\">\n" +
            "                    <i class=\"fas fa-times\"></i>\n" +
            "                </div>\n" +
            "            </div>";

        document.getElementById(receiver + "-notification-close-button").addEventListener('click', (e) => {
            $("#user-notification").alert("close");
            document.getElementById(receiverId).innerHTML = "";
        })

        increaseNotificationNumber();
        setTimeout(dismissNotification, 3000);
        if(type==='friend')
            loadNotification(sender, imageUrl);
    }

    function dismissNotification() {
        $("#user-notification").alert("close");
        document.getElementById(receiverId).innerHTML = "";
    }


    let numberElement = document.getElementById('notification-number');
    console.log(numberElement)

    function increaseNotificationNumber() {
        let numberElement = document.getElementById('notification-number');
        console.log(numberElement)
        if (numberElement.innerHTML.length < 1) {
            numberElement.innerHTML = "1";
        } else {
            numberElement.innerHTML = (parseInt(numberElement.innerHTML) + 1).toString();
        }
    }

    function loadNotification(sender, imageUrl) {
        if (window.location.href.toString().split('/').slice(3).length === 1) {
            let newRequest = document.createElement('div');
            newRequest.classList.add('friend-request')
            newRequest.innerHTML = " <div class=\"user-section\">\n" +
                "                                    <div class=\"friend-user-image\">\n" +
                "                                        <img src=\"" + imageUrl + "\" alt=\"user image\">\n" +
                "                                    </div>\n" +
                "                                </div>\n" +
                "                                <div class=\"request-controls\">\n" +
                "                                    <div class=\"username-wrapper\">\n" +
                "                                        <div class=\"username\">\n" +
                "                                            <a href=\"\">" + sender + "</a>\n" +
                "                                        </div>\n" +
                "                                    </div>\n" +
                "                                    <div class=\"control\">\n" +
                "                                        <div class=\"request-control\" id='confirm-" + sender + "'>\n" +
                "                                            <button type=\"button\" id='confirm-" + sender + "' class=\"btn btn-success confirm-request\">Confirm</button>\n" +
                "                                        </div>\n" +
                "                                        <div class=\"request-control delete-request-button\" >" +
                "                                            <button type=\"button\" id='delete-" + sender + "' class=\"btn btn-danger delete-request\">Delete</button>\n" +
                "                                        </div>\n" +
                "                                    </div>\n" +
                "\n" +
                "                                </div>";

            if ($('.right').children().length <= 0) {
                let friendRequests = document.createElement('div');
                friendRequests.classList.add('friend-requests');

                let requestHeading = document.createElement('h5')
                requestHeading.innerHTML = 'Friend Requests';

                friendRequests.prepend(requestHeading)

                let friendRequestWrapper = document.createElement('div');
                friendRequestWrapper.classList.add('friend-request-wrapper')
                friendRequestWrapper.id = 'friendRequestWrapper';

                friendRequestWrapper.append(newRequest)
                friendRequests.append(friendRequestWrapper)

                $('.right').append(friendRequests);

            } else {
                $('.friend-request-wrapper').prepend(newRequest);

                if ($('.friend-request-wrapper').children().length >= 4) {
                    $(".friend-request:last").remove();
                }
            }
            addEventListenersAcceptFriendRequest();
        }
    }

})