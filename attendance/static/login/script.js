const labels = document.querySelectorAll('.form-control label');

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
        console.log(data);
        if (period === "start"){
            period = data['currentPeriod'];
            console.log('period:', period)
        }
        else {
            if (period === data['currentPeriod']){
                console.log("new period detected");
            }
        }
    }

    checkNewPeriod();
    