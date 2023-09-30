function replaceText(element, text){

    if (element.innerText) {
        element.innerText = text;
    }

    else if (element.textContent) {
        element.textContent = text;
    }
}