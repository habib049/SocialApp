window.addEventListener('load', (event) => {
    let toggle = true;
    document.getElementById('user-options').addEventListener('click', (e) => {
        if (toggle) {
            $('#dropdown-options').slideDown("fast");
            toggle = false;
        } else {
            $('#dropdown-options').slideUp("fast");
            toggle = true;
        }
    });

    document.getElementById('dark-mode-button').addEventListener('click', (e) => {
        document.body.style.filter = "invert(100%)";
    })
});