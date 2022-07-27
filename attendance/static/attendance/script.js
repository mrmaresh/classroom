const studentID = document.querySelector('.student_id');
const yesBtn = document.querySelector('.excused-yes');
const noBtn = document.querySelector('.excused-no');
const previousBtn = document.querySelector('.previous');
const excusedPage = document.querySelector('.excused-container');
const descriptionPage = document.querySelector('.description-container');


let excused;


yesBtn.addEventListener('click', () => {
    excused = true;
    excusedPage.style.display = 'none';
    descriptionPage.style.display = 'block';
})

noBtn.addEventListener('click', () => {
    excused = false;
    excusedPage.style.display = 'none';
    descriptionPage.style.display = 'block';
})

previousBtn.addEventListener('click', () => {
    excusedPage.style.display = 'block';
    descriptionPage.style.display = 'none';
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

