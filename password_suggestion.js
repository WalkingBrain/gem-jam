const pwd = document.getElementById("password");
const len = document.getElementById("len");
const num = document.getElementById("num");
const cap = document.getElementById("cap");

pwd.addEventListener("input", () => {
  const val = pwd.value;
  len.style.color = val.length >= 8 ? "green" : "red";
  num.style.color = /\d/.test(val) ? "green" : "red";
  cap.style.color = /[A-Z]/.test(val) ? "green" : "red";
});
