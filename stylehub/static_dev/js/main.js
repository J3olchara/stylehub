let hearts = document.querySelectorAll('.heart-logic');

for (let i = 0; i < hearts.length; i++) {
    let heart = hearts[i];

    heart.addEventListener('click', async function (evt) {
        heart.classList.toggle('heart')
        heart.classList.toggle('heart-fill')
        await fetch(`/api/toggle_liked/${heart.id}`)
    })
}

window.onload = function() {
    const navigation = document.getElementsByClassName('catalog-item-navigation');
    for (let i = 0; i < navigation.length; ++i) {
        let url = navigation[i].getAttribute('data-url-redirect');
        navigation[i].addEventListener('click', Redirect(url));
    }
    clockUpdate();
    setInterval(clockUpdate, 1000);
}

function change_language_form(form) {
    console.log(form);
    form.submit();
}
