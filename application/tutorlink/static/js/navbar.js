let name_plate = document.getElementById('username-plate');
let dropdown = document.getElementById('user-dropdown');

function open_dropdown()
{
    dropdown.classList.remove('not-visible');
    dropdown.classList.add('is-visible');
    name_plate.innerText = name_plate.innerText.substring(0, name_plate.innerText.length-1)
    name_plate.innerText += "▲";
}

function close_dropdown()
{
    dropdown.classList.remove('is-visible');
    dropdown.classList.add('not-visible');
    name_plate.innerText = name_plate.innerText.substring(0, name_plate.innerText.length-1)
    name_plate.innerText += "▼";
}

function toggle_dropdown()
{
    if(dropdown.classList.contains('not-visible'))
    {
        open_dropdown();
    }
    else
    {
        close_dropdown();
    }
}

document.addEventListener('click', (evt) =>
{
    let clickTarget = evt.target;

    //user clicks on their "welcome, <user>" button
    if(clickTarget === name_plate)
    {
        toggle_dropdown();
    }
    //condition is to prevent accidental closure if user clicks on gap rather than button
    else if(clickTarget !== dropdown)
    {
        close_dropdown();
    }
});
