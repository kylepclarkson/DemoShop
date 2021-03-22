var option = {
    animation: true,
    delay: 4000,
};

function toast() {
    var toastHTMLElement = document.getElementById('toastMessage');
    var toastElement = new bootstrap.Toast(toastHTMLElement, option);

    toastElement.show();
}