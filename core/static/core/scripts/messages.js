document.addEventListener("DOMContentLoaded", function() {
    // Manual close button
    document.querySelectorAll(".close-btn").forEach(btn => {
        btn.addEventListener("click", function() {
            let alert = this.parentElement;
            alert.classList.add("fade-out");
            setTimeout(() => alert.remove(), 500); // match CSS transition
        });
    });

    // Auto-dismiss
    document.querySelectorAll(".alert").forEach(alert => {
        setTimeout(() => {
            alert.classList.add("fade-out");
            setTimeout(() => alert.remove(), 500);
        }, 5000); // disappear after 5s
    });
});