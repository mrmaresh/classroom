const selectEl = document.querySelector(".selectEl");
const selectBtn = document.querySelector(".selectBtn");
const messageEl = document.querySelector(".message-container");

selectBtn.disabled = true;

selectEl.addEventListener('change', () => {
    console.log(selectEl.value);
    if (selectEl.value === "default"){
        selectBtn.disabled = true;
        messageEl.innerHTML = "";
    }
    else{
        selectBtn.disabled = false;
    }

    if (selectEl.value === "Cell Phone Issue"){
        console.log("LKJLKJ");
        messageEl.innerHTML = "Your phone will be sent to the office to be picked up later."
    }
    if (selectEl.value === "Ear Bud Issue"){
        console.log("LKJLKJ");
        messageEl.innerHTML = "Your ear buds will be sent to the office to be picked up later."
    }
});

