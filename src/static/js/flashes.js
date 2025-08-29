const flashContainer = document.querySelector('.flash')
const flashCloseButton = document.querySelector('button.flash-close')

flashCloseButton.onclick = closeFlash

function closeFlash() {
    flashContainer.classList.add('flash-hidden')
}