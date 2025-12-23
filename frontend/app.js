document.getElementById("checkBtn").addEventListener("click", async () => {
    const origin = document.getElementById("origin").value;
    const destination = document.getElementById("destination").value;
    const date = document.getElementById("date").value;

    const resultsEl = document.getElementById("results");
    resultsEl.innerHTML = "Chargement...";

    try {
        const res = await fetch(`/prices?origin=${origin}&destination=${destination}&date=${date}`);
        const data = await res.json();

        if(data.error) {
            resultsEl.innerHTML = data.error;
            return;
        }

        resultsEl.innerHTML = "";
        data.forEach(flight => {
            const li = document.createElement("li");
            li.textContent = `${flight.airline} ${flight.flight_no} - ${flight.price} € | Départ: ${flight.departure} | Arrivée: ${flight.arrival}`;
            resultsEl.appendChild(li);
        });
    } catch (err) {
        resultsEl.innerHTML = "Erreur lors de la récupération des données";
    }
});