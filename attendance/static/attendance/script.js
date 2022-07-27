const studentID = document.querySelector('.student_id');
const yesBtn = document.querySelector('.excused-yes');
const noBtn = document.querySelector('.excused-no');
const previousBtn = document.querySelector('.previous');
const excusedPage = document.querySelector('.excused-container');
const descriptionPage = document.querySelector('.description-container');
const descriptionEl = document.querySelector('.description');
const descriptionBtn = document.querySelector('.description-button');


let excused;

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
    console.log("JJJ");
})

test3();
test4();


async function test3() {
    const response = await fetch('attendance');
    const data = await response.json();
    console.log('test3', data['message']);
}

async function test4(){
    const response = await fetch('attendance',{
        method: 'POST',
        body: JSON.stringify({
            student_id: studentID.innerText
        })
    })
    const data = await response.json();
    console.log('test4', data['message']);
}

