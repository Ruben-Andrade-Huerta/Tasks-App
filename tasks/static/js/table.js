document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll("tr[data-href]").forEach(function(row) {
        row.addEventListener("click", function(e) {
            // Evita que el click en el checkbox dispare la redirección
            if(e.target.tagName.toLowerCase() !== 'input') {
                window.location = this.dataset.href;
            }
        });
        row.style.cursor = "pointer";
    });
});