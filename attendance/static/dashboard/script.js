$(document).ready( function () {
    $('#filter-table').DataTable();
} );

window.onload = displayClock();
function displayClock(){
    var time = new Date().toLocaleTimeString();
    var date = new Date().toDateString();
    document.querySelector('.time').innerHTML = time;
    document.querySelector('.date').innerHTML = date;
    setTimeout(displayClock, 1000);
}