var option = {
    animation: true,
    delay: 2000,
};

// function toast() {
//     var toastHTMLElement = document.getElementById('toastMessage');
//     var toastElement = new bootstrap.Toast(toastHTMLElement, option);
//     toastElement.show();
// }

var toastElList = [].slice.call(document.querySelectorAll('.toast'))
var toastList = toastElList.map(function (toastEl) {
  return new bootstrap.Toast(toastEl, option)
})