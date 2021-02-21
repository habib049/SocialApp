window.addEventListener('load', (event) => {
    alert('i am in')

    setTimeout(changeColor, 2000);

    function changeColor(e) {
        let newNotifications = document.getElementsByClassName('new-notifications')
        if (newNotifications.length > 0) {
            for (let i = 0; i < newNotifications.length; i++) {
                newNotifications[i].style.backgroundColor = '#eeeeee';
            }
        }
    }

});