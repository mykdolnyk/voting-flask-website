const votingForm = document.getElementById("voting-form")
const submitButton = document.getElementById('voting-form-submit')
const pollResultsBlock = document.getElementById('poll-results')
const choiceTemplate = document.getElementById('choice-template')
submitButton.onclick = processSubmission

let tm;

async function processSubmission() {
    displaySubmission()

    if (!tm) {
        tm = await createThumb()
    }

    const formData = new FormData(votingForm)
    formData.append('tm', tm)
    const response = await fetch(submitVoteUrl, {
        'method': 'POST',
        'body': formData
    })
    if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
    }
    const data = await response.json()
    if (data.success) {
        displayPollResults(data)
    }
    else {
        displayVoteFail(data)
    }
}

async function createThumb() {
    await import('https://cdn.jsdelivr.net/npm/@thumbmarkjs/thumbmarkjs/dist/thumbmark.umd.js');
    const tm = new ThumbmarkJS.Thumbmark();
    const result = await tm.get()
    return JSON.stringify(result)
}

function displaySubmission() {
    votingForm.style.display = 'None'
}

function displayPollResults(data) {

    for (choice of data.poll_data.choices) {
        /** @type {DocumentFragment} */
        let frag = choiceTemplate.content.cloneNode(true)

        let newChoice = frag.querySelector('.choice-text')
        newChoice.textContent = choice.text

        let progressbar = frag.querySelector('.progressbar')
        let progressbarBar = progressbar.firstElementChild

        votePercent = (choice.total_votes / data.poll_data.total_votes) * 100
        progressbarBar.style.width = `${votePercent}%`

        pollResultsBlock.appendChild(frag)
        }
}   

function displayVoteFail(data) {
    votingForm.style.display = 'block'
    votingForm.style.backgroundColor = 'red'
    votingForm.appendChild('Error')
}