

test3();
test4();
test5();


async function test3() {
    const response = await fetch('attendance');
    const data = await response.json();
    console.log('test3', data['message']);
}

async function test4(){
    const response = await fetch('attendance',{
        method: 'POST',
        body: JSON.stringify({
            a: 4,
            b: "YO",
            c: 8
        })
    })
    const data = await response.json();
    console.log('test4', data['message']);
}

async function test5(){
    const response = await fetch('attendance',{
        method: 'PUT',
        body: JSON.stringify({
            a: 4,
            b: "YO",
            c: 8
        })
    })
    const data = await response.json();
    console.log('test5', data['message']);
}