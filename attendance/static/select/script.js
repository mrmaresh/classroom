const optionButton = document.querySelector('.option-button');
const restroomButton = document.querySelector('.option-restroom');

optionButton.addEventListener('click', () => {
    optionButton.classList.add('click');
    restroomButton.classList.add('click');
});