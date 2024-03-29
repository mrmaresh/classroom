const labels = document.querySelectorAll('.form-control label');
const waitlistEl = document.querySelector('.waitlist-container');

labels.forEach(label => {
    label.innerHTML = label.innerText
        .split('')
        .map((letter,idx) => `<span style="transition-delay:${idx * 70}ms">${letter}</span>`)
        .join('')
});


    window.onload = displayClock();
    function displayClock(){
        var time = new Date().toLocaleTimeString();
        var date = new Date().toDateString();
        document.querySelector('.time').innerHTML = time;
        document.querySelector('.date').innerHTML = date;
        setTimeout(displayClock, 1000);
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
                clearWaitlist();
                location.reload();
            }
        }
    }


    async function clearWaitlist(){
        const response = await fetch('resetWaitlist',{
            method: 'POST',
            body: JSON.stringify({
                mes: "delete stuff",
            })
        })
        const data = await response.json();
    }

    checkNewPeriod();
    setInterval(checkNewPeriod, 60000);