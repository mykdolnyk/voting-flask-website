const checkUsernameButton = document.getElementById('check-username-button')
const checkedUsernameInput = document.getElementById('check-username-input')
const checkedUsername = document.getElementById('checked-username')
const chosenOption = document.getElementById('chosen-option')
const checkUsernameResultBox = document.getElementById('check-username-result-box')

const checkVotersButton = document.getElementById('check-voters-button')
const checkVotersList = document.getElementById('admin-user-list')

checkUsernameButton.onclick = checkUsername
checkVotersButton.onclick = checkVoters

let votersPage = 1

async function checkUsername() {
    const username = checkedUsernameInput.value

    const response = await fetch(`${checkUsernameUrl}?poll-id=${pollId}`.replace("__USERNAME__", username))
    const result = await response.json()

    let retrievedUsername = result.username
    let retrievedChoice = Object.values(result.choices)[0]

    if (!retrievedChoice)
    {
        return 0
    }

    checkedUsername.textContent = retrievedUsername
    chosenOption.textContent = retrievedChoice

    checkUsernameResultBox.classList.remove('hidden')

    return 0
}


async function checkVoters() {
    const response = await fetch(`${checkVotersUrl}?page=${votersPage}`)
    const result = await response.json()
    
    if (Object.keys(result.voters).length === 0) {
        checkVotersButton.disabled = true
        return 0
    }
    votersPage++

    for (let voter in result.voters) {
        voterItem = document.createElement('li')
        voterItem.textContent = voter
        checkVotersList.appendChild(voterItem)
    }

    return 0
}