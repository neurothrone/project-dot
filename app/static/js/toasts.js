window.onload = (event) => {
    let alert = document.querySelector(".toast");
    if (alert) {
        let bootstrapAlert = new bootstrap.Toast(alert);
        bootstrapAlert.show();
    }
}