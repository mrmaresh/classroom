$(document).ready( function () {
    $('#filter-table').DataTable();
} );

const resetAbsencesButton = document.querySelector('#reset-absences');
const resetButton = document.querySelector('#reset-button');
const pickStudentButton = document.querySelector('#pick-student');
const okResponseButton = document.querySelector('#ok-response');
const absentButton = document.querySelector('#absent');
const studentNameEl = document.querySelector('.student-name');
const studentIdEl = document.querySelector('.student-id');
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

resetAbsencesButton.addEventListener('click', () => {
    console.log('clicked resetAbsencesButton');
    resetAbsences();
})

pickStudentButton.addEventListener('click', () => {
    console.log('clicked pickStudentButton');
    randomStudent();
})


okResponseButton.addEventListener('click', () => {
    console.log('clicked okResponseButton');
    console.log(studentIdEl.innerHTML);
    responseCount();
})

absentButton.addEventListener('click', () => {
    console.log('clicked absentButton');
    recordAbsence();
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
    console.log(data['name']);
    console.log(data['student_id'])
    studentNameEl.innerHTML = data['name'];
    studentIdEl.innerHTML = data['student_id']
}

async function responseCount(){
    const response = await fetch('randomStudent',{
        method: 'POST',
        body: JSON.stringify({
            student_id: studentIdEl.innerHTML,
        })
    })
    const data = await response.json();
}


async function resetAbsences(){
    const response = await fetch('resetAbsences',{
        method: 'POST',
        body: JSON.stringify({
            mes: "reset stuff",
        })
    })
    const data = await response.json();
}


async function recordAbsence(){
    const response = await fetch('recordAbsence', {
        method: 'POST',
        body: JSON.stringify({
            student_id: studentIdEl.innerHTML,
        })
    })
    const data = await response.json();
}


let period = "start";
async function checkNewPeriod() {
    const response = await fetch('checkNewPeriod');
    const data = await response.json();
    currentPeriod = data['currentPeriod'];
    console.log("period = ", period, ", currentPeriod = ", currentPeriod);
    if (period === "start"){
        period = currentPeriod;
        console.log('period:', period)
    }
    else {
        if (period === currentPeriod){
            console.log("No change detected");
        }
        else{
            console.log("new period detected");
            period = currentPeriod;
            resetAbsences();
            location.reload();
        }
    }
}

checkNewPeriod();
setInterval(checkNewPeriod, 60000);