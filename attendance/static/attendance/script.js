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
const consequence1 = document.querySelector('.consequence-warning');
const consequence2 = document.querySelector('.consequence-lunch-detention');
const consequence3 = document.querySelector('.consequence-after-school-detention');
const consequence4 = document.querySelector('.consequence-referral');


let excused;
let description;
let numTardies = unexcusedTardies();

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
    if (numTardies === 0){
        consequence1.style.display = 'none';
    }
    else if (numTardies === 1){
        consequence2.style.display = 'none';
    }
    else if (numTardies === 2){
        consequence3.style.display = 'none';
    }
    else if (numTardies > 2){
        consequence4.style.display = 'none';
    }
})







async function unexcusedTardies() {
    const response = await fetch('unexcused/'.concat(studentID.innerText));
    const data = await response.json();
    console.log(data['numTardies'] > 2)
    return data['numTardies']
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
    console.log('recordTardy', data);
}

