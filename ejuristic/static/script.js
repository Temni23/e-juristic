let page = document.querySelector('.page');
let themeButton = document.querySelector('.theme-button');

themeButton.onclick = function () {
    page.classList.toggle('light-theme');
    page.classList.toggle('dark-theme');
};

// Получаем необходимые элементы
var modal = document.getElementById("myModal");
var btn = document.getElementById("openModal");
var span = document.getElementsByClassName("close")[0];

// Открываем модальное окно при клике на кнопку
btn.onclick = function () {
    modal.style.display = "block";
}

// Закрываем модальное окно при клике на крестик
span.onclick = function () {
    modal.style.display = "none";
}

// Закрываем модальное окно при клике вне его
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}