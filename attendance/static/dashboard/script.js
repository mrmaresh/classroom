$(document).ready( function () {
    $('#filter-table').DataTable();
} );

resetButton = document.querySelector('#reset-button');
timeEl = document.querySelector('#time');
dateEl = document.querySelector('#date');

const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

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

    timeEl.innerHTML = `${hoursForClock}:${minutes < 10 ? `0${minutes}` : minutes}:${seconds < 10 ? `0${seconds}` : seconds} ${ampm}`;
    dateEl.innerHTML = `${days[day]}, ${months[month]} <span class="circle">${date}</span>`;
}

resetButton.addEventListener('click', () => {
    console.log('clicked')
    clearWaitlist();
})
setInterval(setTime, 1000);



async function clearWaitlist(){
    const response = await fetch('resetWaitlist',{
        method: 'POST',
        body: JSON.stringify({
            mes: "delete stuff",
        })
    })
    const data = await response.json();
}
