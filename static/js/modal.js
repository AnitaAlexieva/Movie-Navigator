let listsData = []; // ще пази твоите списъци

function openModal(movieId) {
    const modal = document.getElementById("listModal");
    modal.style.display = "block";
    document.getElementById("modal_movie_id").value = movieId;
    loadLists(); // ако имаш функция за зареждане на списъците
}

function closeModal() {
    document.getElementById("listModal").style.display = "none";
}

window.onclick = function(event) {
    const modal = document.getElementById("listModal");
    if (event.target == modal) modal.style.display = "none";
}

// Зареждане на списъците от backend
async function loadLists() {
    const response = await fetch('/lists/json'); // нов endpoint
    listsData = await response.json();
    const container = document.getElementById("lists-container");
    container.innerHTML = "";
    listsData.forEach(list => {
        const btn = document.createElement("button");
        btn.textContent = list.name;
        btn.onclick = () => addMovieToList(list.id);
        container.appendChild(btn);
    });
}

// Добавяне на филм в съществуващ списък
async function addMovieToList(listId) {
    const movieId = document.getElementById("modal_movie_id").value;
    const formData = new FormData();
    formData.append('movie_id', movieId);

    // 🚨 Забележи, че тук извикваме JSON endpoint
    const response = await fetch(`/lists/${listId}/add_movie/json`, {
        method: 'POST',
        body: formData
    });

    // Вече получаваме валиден JSON
    const result = await response.json();
    alert(result.status === "added" ? "Филмът е добавен!" : "Вече е в списъка!");

    closeModal();
}

// Създаване на нов списък и добавяне на филм
async function createListAndAddMovie() {
    const name = document.getElementById("new_list_name").value;
    const description = document.getElementById("new_list_description").value;
    const movieId = document.getElementById("modal_movie_id").value;

    // 1️⃣ Създаваме нов списък
    const createResp = await fetch('/lists/create/json', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name, description})
    });
    const newList = await createResp.json();

    // 2️⃣ Добавяме филма към новия списък (JSON endpoint!)
    const formData = new FormData();
    formData.append('movie_id', movieId);

    const addResp = await fetch(`/lists/${newList.id}/add_movie/json`, {
        method: 'POST',
        body: formData
    });
    const result = await addResp.json();

    alert(result.status === "added" ? "Филмът е добавен!" : "Вече е в списъка!");
    closeModal();
}

async function _removeMovieFromListApi(listId, movieId) {
    const form = new FormData();
    form.append('movie_id', movieId);

    const resp = await fetch(`/lists/${listId}/remove_movie/json`, {
        method: 'POST',
        body: form
    });

    let data = {};
    try {
        data = await resp.json();
    } catch (e) {
        data = {status: 'error', message: 'Invalid JSON from server'};
    }

    return { ok: resp.ok, data };
}

// --------------------
// ПРЕМАХВАНЕ НА ФИЛМ ОТ СПИСЪК (ГЛОБАЛНО ДОСТЪПНО)
// --------------------
window.removeMovieFromList = async function(listId, movieId, btn) {
    if (!confirm("Сигурен ли си, че искаш да премахнеш този филм?")) return;

    try {
        const result = await _removeMovieFromListApi(listId, movieId);

        if (result.ok && result.data.status === 'removed') {
            const card = btn.closest('.movie-card'); // използваме бутона, който е кликнат
            if (card) card.remove(); // премахваме от DOM
        } else {
            alert('Грешка при премахване на филма.');
        }
    } catch (err) {
        console.error("Грешка при премахване на филм:", err);
        alert("Възникна грешка при свързване със сървъра.");
    }
};

// Добавяме слушатели на бутоните
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.remove-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const listId = btn.dataset.list;
            const movieId = btn.dataset.movie;
            removeMovieFromList(listId, movieId, btn); // предаваме бутона
        });
    });
});


