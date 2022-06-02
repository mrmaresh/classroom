

document.addEventListener('DOMContentLoaded', function() {

    window.onload = displayClock();
    function displayClock(){
        var time = new Date().toLocaleTimeString();
        var date = new Date().toDateString();
        document.getElementById('txt').innerHTML = time ;
        setTimeout(displayClock, 1000);
    }













});



