async function loadPrices() {
    const resultsEl = document.getElementById("results");
    resultsEl.innerHTML = "Chargement...";
    try {
        const res = await fetch("/prices");
        const data = await res.json();
        resultsEl.innerHTML = "";
        data.forEach(flight => {
            const li = document.createElement("li");
            li.textContent = `${flight.origin} -> ${flight.destination} | ${flight.date} | ${flight.airline} ${flight.flight_no} : ${flight.price} €`;
            if (flight.alert) {
                li.classList.add("alert");
                li.textContent = "⚠️ " + li.textContent;
            }
            resultsEl.appendChild(li);
        });
    } catch {
        resultsEl.innerHTML = "Erreur lors du chargement";
    }
}

document.getElementById("refresh").addEventListener("click", loadPrices);

loadPrices(); // Chargement initial
