const pollForm = document.getElementById("admin-form");
const choiceSection = document.getElementById("admin-choice-form-section");
const addChoiceButton = document.getElementById("add-choice-button");

addChoiceButton.onclick = addNewChoiceField;

function addNewChoiceField() {
    let field = choiceSection.firstElementChild.cloneNode(true)

    for (const child of field.childNodes) {
        let choiceNumber = choiceSection.querySelectorAll("input[type='text']").length;

        if (child.tagName === 'INPUT' && child.type === 'text') {
            child.value = '';
            child.id = `choices-${choiceNumber}-text`;
            child.name = `choices-${choiceNumber}-text`;
        } 
        else if (child.tagName === 'LABEL') {
            child.for = `choices-${choiceNumber}-text`;
        }
    }



    choiceSection.appendChild(field)

    console.log('added new field');
}