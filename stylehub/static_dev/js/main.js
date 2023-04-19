let hearts = document.querySelectorAll('.heart-logic');

for (let i = 0; i < hearts.length; i++) {
    let heart = hearts[i];

    heart.addEventListener('click', async function (evt) {
        heart.classList.toggle('heart')
        heart.classList.toggle('heart-fill')
        await fetch(`/api/toggle_liked/${heart.id}`)
    })
}