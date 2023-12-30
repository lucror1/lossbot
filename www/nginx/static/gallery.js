function openModal(evt) {
    // Filter non-enter keypresses
    if (evt.key !== undefined && evt.key !== "Enter") {
        return;
    }

    // Get the background image
    let target = evt.target;

    let url;
    if (target.style.backgroundImage) {
        url = target.style.backgroundImage;
        url = url.substring(5, url.length-2);
    } else {
        url = target.src;
    }

    let img = document.querySelector("#modal img");
    img.src = url;

    document.querySelector("#modal").style.display = "block";

    evt.stopPropagation();
}

function closeModal(evt) {
    if (!isActionEvt(evt)) {
        return;
    }

    document.querySelector("#modal").style.display = "none";
}

// Determine if the given event is a "action" event (click or enter)
// Alternatively, return true if no evt was provided (i.e., this function was called manually)
function isActionEvt(evt) {
    return evt === undefined || evt.key === undefined || evt.key === "Enter";
}

document.addEventListener("DOMContentLoaded", () => {
    // Make each thumbnail expand on click
    let thumbnails = document.querySelectorAll(".thumbnail");
    for (let t of thumbnails) {
        t.addEventListener("click", openModal);
        t.addEventListener("keydown", openModal);
    }

    // Add event listeners for close button
    let close = document.querySelector("#modal-close");
    close.addEventListener("click", closeModal);
    close.addEventListener("keydown", closeModal);

    // Clicking outside of the modal content closes the modal
    document.querySelector("#modal").addEventListener("click", () => {
        closeModal();
    });
    document.querySelector(".modal-content").addEventListener("click", (evt) => {
        evt.stopPropagation();
    })
});