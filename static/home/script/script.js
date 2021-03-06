window.addEventListener('load', (event) => {


    var infinite = new Waypoint.Infinite({
        element: $('.infinite-container')[0],

        offset: 'bottom-in-view',

        onBeforePageLoad: function () {
            $('.loading').show();
        },
        onAfterPageLoad: function () {
            $('.loading').hide();
        }

    });


    let carousel = $(".carousel");
    $(".carousel-control-prev").click(function (e) {
        e.preventDefault();
        carousel.carousel("prev");
        carousel.carousel("dispose");
    });

    $(".carousel-control-next").click(function (e) {
        e.preventDefault();
        carousel.carousel("next");
        carousel.carousel("dispose");
    });

    // comments processing

    let commentsDisplay = document.getElementsByClassName('display-comments');

    for (let i = 0; i < commentsDisplay.length; i++) {
        commentsDisplay[i].addEventListener('click', loadComments);
    }


    function loadComments(e, updateCommentNumber = false) {
        e.preventDefault();
        $.ajax({
            type: 'GET',
            data: {
                'post_id': this.id.toString().split("-")[2]
            },
            url: 'create-post/get-comments',
            dataType: 'json',
            success: function (data) {
                let comments = data['comments'];
                let commentDisplayData = "";
                let i = 0, j = 0;
                let maxSize = 0;
                let className = "";
                let marginLeft = 0;
                let parentComment;
                let timeAgo;

                let commentObject = comments[i];
                while (true) {
                    className = "level-" + commentObject.comment_level;
                    marginLeft = (commentObject.comment_level * 32) + "px";
                    timeAgo = timeSince(commentObject.add_time)


                    commentDisplayData += "<div class=\"comment-wrapper " + className + "\" style=\"margin-left:" + marginLeft + " \">\n" +
                        "                                        <div class=\"main-comment-section\">\n" +
                        "                                            <div class=\"user-comment-image\">\n" +
                        "                                                <img src=\"" + commentObject.image_url + "\" alt=\"\">\n" +
                        "                                            </div>\n" +
                        "                                            <div class=\"comment-content-user-info\">\n" +
                        "                                                <div class=\"username\">\n" +
                        "                                                    <a href=\"\">" + commentObject.username + "</a>\n" +
                        "                                                </div>\n" +
                        "                                                <div class=\"comment-content\">\n" +
                        "                                                    <p>" + commentObject.content + "</p>\n" +
                        "                                                </div>\n" +
                        "                                            </div>\n" +
                        "                                        </div>                                        \n" +
                        "                                        <div class=\"comment-controls\">\n" +
                        "                                            <p class='comment-reply'><span id='reply-button-" + commentObject.id + "' class='reply-comment'>Reply</span>  - " + timeAgo + " ago</p>\n" +
                        "                                        </div>\n" +
                        "<div class='reply-comment-section' id='reply-" + commentObject.id + "'>" +
                        "<form method=\"post\"  class=\"reply-comment-form\"\n" +
                        "                                  id=\"form-" + commentObject.id + "\">\n" +

                        "                                <div class=\"input-field comment-input-field\">\n" +

                        "                                        <input type=\"text\" name=\"reply_comment\" class=\" reply-comment-input\"\n" +
                        "                                               placeholder=\"Write reply comment\">\n" +

                        "                                </div>\n" +
                        "                            </form>" +
                        "                                   </div>" +
                        "                                    </div>"

                    if (commentObject.replies.length > 0) {
                        j = 0;
                        maxSize = 0;
                        maxSize = commentObject.replies.length;
                        parentComment = commentObject;
                    }
                    if (j < maxSize) {
                        commentObject = parentComment.replies[j];
                        j++;
                    } else {
                        i++;
                        if (i < comments.length) {
                            commentObject = comments[i];
                        } else {
                            break;
                        }
                    }
                }
                let commentDisplayId = "comment-display-" + commentObject.post_id;
                document.getElementById(commentDisplayId).innerHTML = commentDisplayData;

                if (updateCommentNumber)
                    updateCommentValue(commentsDisplay.id)

                addListenersToReplyButton();
                addListenersToReplyForms();
            },
            error: function (e) {
                console.log(e)
            }
        });
    }

    // applying event listener to new comments form
    let forms = document.getElementsByClassName("comment-form");
    for (let i = 0; i < forms.length; i++) {
        forms[i].addEventListener('submit', postNewComment)
    }

    function postNewComment(e) {
        let form = this.id;
        let inputField = this.comment;
        e.preventDefault();
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            type: 'POST',
            data: {
                'comment': this.comment.value,
                'post': form,
            },

            url: this.getAttribute('data-url'),
            dataType: 'json',
            success: function (data) {
                loadComments(e, true);
                inputField.value = "";
                inputField.blur();
            }
        });
    }


    function addListenersToReplyButton(e) {
        let replyButtons = document.getElementsByClassName('reply-comment');
        for (let i = 0; i < replyButtons.length; i++) {
            replyButtons[i].addEventListener('click', enableReplyForm);
        }
    }

    function addListenersToReplyForms(e) {
        let replyforms = document.getElementsByClassName('reply-comment-form');
        for (let i = 0; i < replyforms.length; i++) {
            replyforms[i].addEventListener('submit', postReplyComment);
        }
    }

    function enableReplyForm(e) {
        let postId = this.id.toString().split('-')[2];
        let formId = "reply-" + postId;
        let form = document.getElementById(formId);
        if (form.style.display === 'block')
            form.style.display = 'none';
        else
            form.style.display = 'block';
    }

    function postReplyComment(e) {
        let form = this.id;
        e.preventDefault();

        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            type: 'POST',
            data: {
                'comment': this.reply_comment.value,
                'parentId': this.id.toString().split('-')[1],
            },

            url: '/create-post/post-reply-comment',
            dataType: 'json',
            success: function (data) {
                loadComments(e, true);
            }
        });
    }

    function updateCommentValue(id) {
        let commentLabel = document.getElementById(id)
        let commentNumber = commentLabel.innerHTML.toString().split(' ')[0];
        commentLabel.innerHTML = (parseInt(commentNumber) + 1) + " comments";
    }

    function timeSince(timeStamp) {
        let date = (timeStamp.toString().split('T')[0]);
        let time = timeStamp.toString().split('T')[1].substring(0, 8);
        var newTimeStamp = new Date(date + " " + time)

        var now = new Date(), secondsPast = (now.getTime() - newTimeStamp) / 1000;
        if (secondsPast < 60) {
            return parseInt(secondsPast) + 's';
        }
        if (secondsPast < 3600) {
            return parseInt(secondsPast / 60) + 'm';
        }
        if (secondsPast <= 86400) {
            return parseInt(secondsPast / 3600) + 'h';
        }
        if (secondsPast > 86400) {
            day = newTimeStamp.getDate();
            month = newTimeStamp.toDateString().match(/ [a-zA-Z]*/)[0].replace(" ", "");
            year = newTimeStamp.getFullYear() === now.getFullYear() ? "" : " " + newTimeStamp.getFullYear();
            return day + " " + month + year;
        }
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

    //likes processing
    // adding listeners to like buttons
    let buttons = document.getElementsByClassName('like-buttons');
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener('click', updateLike)
    }

    function updateLike(e) {
        e.preventDefault();
        let likeLabel = this;
        let postId = this.id.toString().split('-')[1]
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            type: 'POST',
            data: {
                'postId': postId
            },

            url: 'create-post/like-post',
            dataType: 'json',
            success: function (data) {
                if (data['update'] === true) {
                    likeLabel.style.color = 'blue';
                } else {
                    likeLabel.style.color = 'black';
                }
                let likeNumberLabelId = 'like-number-' + postId;
                let likeNumberLabel = document.getElementById(likeNumberLabelId)
                likeNumberLabel.innerHTML = data['likes'] + " like this post";

            }
        });
    }

    //adding event listeners to like numbers display yot shows who like this post
    let likeLabels = document.getElementsByClassName('like-number-display')
    for (let i = 0; i < likeLabels.length; i++) {
        likeLabels[i].addEventListener('click', loadLikeUsers)
    }

    function loadLikeUsers(e) {
        e.preventDefault();
        let postId = this.id.toString().split('-')[2]
        let modalContentId = "modal-content-" + postId;
        let modalContent = document.getElementById(modalContentId)
        $.ajax({
            type: 'GET',
            data: {
                'postId': postId
            },
            url: '/create-post/post-like-users',
            dataType: 'json',
            success: function (data) {
                let userData = data['users']
                modalContent.innerHTML = "";
                for (let i = 0; i < userData.length; i++) {
                    modalContent.innerHTML += "<div class=\"user-section\">\n" +
                        "                                        <div class=\"user-image\">\n" +
                        "                                            <img src=\"" + userData[i].image_url + "\" alt=\"user image\">\n" +
                        "                                        </div>\n" +
                        "                                        <div class=\"username\">\n" +
                        "                                            <a href=\"\">" + userData[i].username + "</a>\n" +
                        "                                        </div>\n" +
                        "                                    </div>";
                }
                let modalId = "modal-" + postId
                console.log(modalId)
                $('#' + modalId).modal('show');
            },
            error(e) {
                console.log(e)
            }
        });
    }


    //adding ajax in search
    document.getElementById('search-from').addEventListener('submit', (e) => {
        e.preventDefault();
        $.ajax({
            type: 'GET',
            url: '/search/' + $('#searchProfilesInput').val(),
            data: $("#search-from").serialize(),
            dataType: 'html',
            success: function (data) {
                let newUrl = "/search/" + $('#searchProfilesInput').val()
                $('.application').html(data)
                // changing the url
                window.history.replaceState('', 'Search', newUrl);
            },
            error: () => {
                alert("error occured")
            }
        });
    })

    // document.getElementById('btn').addEventListener('click', (e) => {
    //     e.preventDefault();
    //     $.ajax({
    //         type: 'GET',
    //         url: '/search/temp/temp/habib',
    //         dataType: 'html',
    //         success: function (data) {
    //             console.log(data)
    //             $('.application').html(data)
    //         },
    //         error: () => {
    //             alert("error occured")
    //         }
    //     });
    // })
});