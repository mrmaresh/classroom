const studentID = document.querySelector('.student_id');


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

