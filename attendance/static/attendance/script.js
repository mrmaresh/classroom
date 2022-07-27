const studentID = document.querySelector('.student_id');
const yesBtn = document.querySelector('.excused-yes');
const noBtn = document.querySelector('.excused-no');
const previousBtn = document.querySelector('.previous');
const excusedPage = document.querySelector('.excused-container');
const descriptionPage = document.querySelector('.description-container');
const descriptionEl = document.querySelector('.description');
const descriptionBtn = document.querySelector('.description-button');
const policyPage = document.querySelector('.policy-container');
const returnPage = document.querySelector('.return-container');
const consequencePage = document.querySelector('.consequence-container');
const policyBtn = document.querySelector('.policy-button');
const message = document.querySelector('.return-excused-message');


let excused;
let description;

descriptionBtn.disabled = true;

yesBtn.addEventListener('click', () => {
    excused = true;
    excusedPage.style.display = 'none';
    descriptionPage.style.display = 'block';
    descriptionEl.focus();
})


noBtn.addEventListener('click', () => {
    excused = false;
    excusedPage.style.display = 'none';
    descriptionPage.style.display = 'block';
    descriptionEl.focus();
})


previousBtn.addEventListener('click', () => {
    excusedPage.style.display = 'block';
    descriptionPage.style.display = 'none';
})


descriptionEl.addEventListener('keyup', () => {
    if (descriptionEl.value === ''){
        descriptionBtn.disabled = true;
    }
    else{
        descriptionBtn.disabled = false;
    }
})

descriptionBtn.addEventListener('click', () => {
    descriptionPage.style.display = 'none';
    if (excused === true) {
        returnPage.style.display = 'block';
    }
    else{
        policyPage.style.display = 'block';
    }
    description = descriptionEl.value;
    recordTardy();
})

policyBtn.addEventListener('click', () => {
    policyPage.style.display = 'none';
    consequencePage.style.display = 'block';
    returnPage.style.display = 'block';
    message.style.display = 'none';
})


test3();



async function test3() {
    const response = await fetch('attendance');
    const data = await response.json();
    console.log('test3', data['message']);
}

async function recordTardy(){
    const response = await fetch('attendance',{
        method: 'POST',
        body: JSON.stringify({
            student_id: studentID.innerText,
            reason: description,
            excused: excused
        })
    })
    const data = await response.json();
    console.log('test4', data);
}

