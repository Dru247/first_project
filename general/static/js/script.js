let change_login = document.querySelector('.wialon-login');
let input_login = document.querySelector('.change-wia-login');
let login_button = document.querySelector('.button-change-wia-login')

login_button.onclick = function() {
  change_login.textContent = input_login.value;
};


let change_password = document.querySelector('.wialon-password');
let input_password = document.querySelector('.change-wia-password');
let password_button = document.querySelector('.button-change-wia-password')

password_button.onclick = function() {
  change_password.textContent = input_password.value;
};

/* function copyValue(elementId) {
//    Get the text field
  var copyText = document.getElementById(elementId).innerHTML;
  console.log(copyText);
//   Select the text field
  copyText.select();
//   Copy the text inside the text field
  document.execCommand("copy");
} */

//let copy_pass_2 = document.querySelector('.copy-pass-2');

//copy_pass_2.onclick = copyToClipboard('#copy-test');
