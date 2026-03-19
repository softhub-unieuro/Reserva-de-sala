const loginForm = document.getElementById("loginForm");
const raInput = document.getElementById("ra");

raInput.addEventListener("input", function (e) {
  let value = e.target.value.replace(/\D/g, "");
  if (value.length > 6) {
    value = value.slice(0, 6);
  } 
  e.target.value = value;
});

loginForm.addEventListener("submit", function (event) {
  event.preventDefault();

  const ra = raInput.value;
  const password = document.getElementById("password").value;

  if (ra.length !== 6) {
    alert("O RA deve ter exatamente 6 dígitos.");
    return;
  }

  console.log("Formulário enviado:");
  console.log("RA:", ra);
  console.log("Senha:", "********");
});
