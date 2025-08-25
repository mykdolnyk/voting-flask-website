const pollList = document.getElementById("poll-list")
const pollCardTemplate = document.getElementById("poll-card-template")
const loadMoreButton = document.getElementById("load-more-button")

loadMoreButton.onclick = loadMorePolls

var currentPage = 1

loadPolls(currentPage)

async function loadPolls(page = 1) {
    const response = await fetch(`${requestUrl}?page=${page}`)
    const results = await response.json()

    if (results.length <= 0) {
        disableButton(loadMoreButton)
        return 1
    }
    
    for (let result of results) {
        /**
         * @type {DocumentFragment}
         */
        let pollCard = pollCardTemplate.content.cloneNode(true)

        pollCard.querySelector('.poll-title').innerHTML = result.title
        pollCard.querySelector('.poll-total-votes').innerHTML = result.total_votes
        pollCard.querySelector('.poll-ended-on').innerHTML = result.expires_on
        pollCard.querySelector('.poll-winner').innerHTML = result.current_winner
        pollCard.querySelector('.button').href = result.url

        pollList.appendChild(pollCard)
    }
    currentPage += 1
}

async function loadMorePolls() {
    loadPolls(currentPage)
}

function disableButton(button) {
    button.disabled = true
}