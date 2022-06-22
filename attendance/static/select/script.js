const optionButton = document.querySelector('.option-button');
const restroomButton = document.querySelector('.option-restroom');
const homeButton = document.querySelector('.option-home');
const welcome = document.querySelector('.welcome');

optionButton.addEventListener('click', () => {
    optionButton.classList.add('click');
    restroomButton.classList.add('click');
    homeButton.classList.add('click');
});

document.addEventListener("DOMContentLoaded", function(){
    fontSize();
});


function fontSize(){
    welcome.classList.add('grow');
}