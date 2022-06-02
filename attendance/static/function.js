

document.addEventListener('DOMContentLoaded', function() {

    window.onload = displayClock();
    function displayClock(){
        var time = new Date().toLocaleTimeString();
        var date = new Date().toDateString();
        document.getElementById('time').innerHTML = time;
        document.getElementById('date').innerHTML = date;
        setTimeout(displayClock, 1000);
    }













});



