if (document.querySelector('.option-button') != null){
    const optionButton = document.querySelector('.option-button');
    const restroomButton = document.querySelector('.option-restroom');
    const homeButton = document.querySelector('.option-home');

    console.log(optionButton);

    optionButton.addEventListener('click', () => {
        optionButton.classList.add('click');
        restroomButton.classList.add('click');
        restroomButton.style.display = 'block';
        homeButton.classList.add('click');
        homeButton.style.display = 'block';
    });
}

const welcome = document.querySelector('.welcome');
document.addEventListener("DOMContentLoaded", function(){
    fontSize();
});

function fontSize(){
    welcome.classList.add('grow');
}