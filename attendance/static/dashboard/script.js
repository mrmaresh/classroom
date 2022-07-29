$(document).ready( function () {
    $('#filter-table').DataTable();
} );

timeEl = document.querySelector('#time');
dateEl = document.querySelector('#date');

function setTime() {
    const time = new Date();
    const month = time.getMonth();
    const date = time.getDate();
    const day = time.getDay();
    const hours = time.getHours();
    const hoursForClock = hours % 12;
    const minutes = time.getMinutes();
    const seconds = time.getSeconds();

    const ampm = hours < 12 ? 'AM' : 'PM';

    hourEl.style.transform = `translate(-50%, -100%) rotate(${(360/12)*hours}deg)`;
    minuteEl.style.transform = `translate(-50%, -100%) rotate(${(360/60)*minutes}deg)`;
    secondEl.style.transform = `translate(-50%, -100%) rotate(${(360/60)*seconds}deg)`;

    timeEl.innerHTML = `${hoursForClock}:${minutes < 10 ? `0${minutes}` : minutes} ${ampm}`;
    dateEl.innerHTML = `${days[day]}, ${months[month]} <span class="circle">${date}</span>`;
}

setInterval(setTime, 1000);




