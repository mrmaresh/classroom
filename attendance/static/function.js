

document.addEventListener('DOMContentLoaded', function() {

    window.onload = displayClock();
    function displayClock(){
        var display = new Date().toLocaleTimeString();
        document.getElementById('txt').innerHTML = display;
        setTimeout(displayClock, 1000);
    }
});



