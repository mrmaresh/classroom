const selectEl = document.querySelector(".selectEl");
const selectBtn = document.querySelector(".selectBtn");
const messageEl = docmument.querySelector(".message");

selectBtn.disabled = true;

selectEl.addEventListener('change', () => {
    if (selectEl.value === "default"){
        selectBtn.disabled = true;
    }
    else{
        selectBtn.disabled = false;
    }

    if (selectEl.value === )
});

