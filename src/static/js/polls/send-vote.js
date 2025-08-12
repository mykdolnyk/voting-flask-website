let votingForm = document.getElementById("voting-form")
let submitButton = document.getElementById('voting-form-submit')

submitButton.onclick = sendData

var tm

import('https://cdn.jsdelivr.net/npm/@thumbmarkjs/thumbmarkjs/dist/thumbmark.umd.js').then(() => {
    const fp = new ThumbmarkJS.Thumbmark();
    fp.get().then((res) => {
        tm = JSON.stringify(res)
    })
})

function sendData() {
    let formData = new FormData(votingForm)
    formData.append('tm', tm)
    fetch(submitVoteUrl, {
        'method': 'POST',
        'body': formData
    })
    .then((res) => {return res.json()})
    .then(data => {
        console.log(data)
    })
}
