text = ['Blog', 'Ads', 'Content']
function animateText(words) {
    const outputElement = document.getElementById("textchange");
    let wordIndex = 0;
    let charIndex = 0;
    let isAdding = true;

    const interval = setInterval(() => {
        if (isAdding) {
            if (charIndex < words[wordIndex].length) {
                outputElement.innerHTML += words[wordIndex][charIndex];
                charIndex++;
            } else {
                isAdding = false;
                charIndex--; // Start removing from the last character
            }
        } else {
            if (charIndex >= 0) {
                outputElement.innerHTML = outputElement.innerHTML.slice(0, -1);
                charIndex--;
            } else {
                isAdding = true;
                wordIndex = (wordIndex + 1) % words.length;
                charIndex = 0;
            }
        }
    }, 500);
}
$(document).ready(function () {
    $(".owl-carousel").owlCarousel({
        items: 3,
        loop: true,
        autoplay: true,
        autoplayTimeout: 3000,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 1
            },
            1100: {
                items: 3
            }
        },
        margin: 10
    });
});
animateText(text)

