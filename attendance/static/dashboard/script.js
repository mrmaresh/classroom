$(document).ready( function () {
    $('#filter-table').DataTable();
} );

const resetButton = document.querySelector('#reset-button');
const pickStudentButton = document.querySelector('#pick-student');
const okResponseButton = document.querySelector('#ok-response');
const tryAgainButton = document.querySelector('#try-again');
const absentButton = document.querySelector('#absent');
const studentNameEl = document.querySelector('.student-name');
const timeEl = document.querySelector('#time');
const dateEl = document.querySelector('#date');

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
    location.reload();
})

pickStudentButton.addEventListener('click', () => {
    console.log('clicked pickStudentButton');
    randomStudent();
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

async function randomStudent(){
    const response = await fetch('randomStudent');
    const data = await response.json();
    console.log(data);
}