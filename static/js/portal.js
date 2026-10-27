/**
 * Static JavaScript Demo for Student Portal
 * Path: static/js/portal.js
 * Loaded via: {% load static %} and {% static 'js/portal.js' %}
 */

document.addEventListener("DOMContentLoaded", () => {
    console.log("🚀 Static JS loaded successfully from: static/js/portal.js");

    // 1. Image preview modal when clicking on any QuickGraph
    const graphImages = document.querySelectorAll(".graph-card-img");
    graphImages.forEach((img) => {
        img.addEventListener("click", () => {
            // Open full-sized graph in a new tab or inspect
            window.open(img.src, "_blank");
        });
    });

    // 2. Real-time table filter highlight (if search input exists)
    const searchInput = document.querySelector("input[name='q']");
    if (searchInput) {
        searchInput.addEventListener("focus", () => {
            searchInput.parentElement.classList.add("shadow-sm");
        });
        searchInput.addEventListener("blur", () => {
            searchInput.parentElement.classList.remove("shadow-sm");
        });
    }

    // 3. Auto-dismiss alerts after 4 seconds if any are present
    const alerts = document.querySelectorAll(".alert-dismissible");
    alerts.forEach((alert) => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 4000);
    });
});
