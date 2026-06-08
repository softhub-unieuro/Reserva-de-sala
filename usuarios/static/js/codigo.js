const codeForm = document.getElementById("codeForm");
const accessCodeInput = document.getElementById("accessCode");
const message = document.getElementById("message");

accessCodeInput.addEventListener("input", function (e) {
  let value = e.target.value.replace(/\D/g, "");
  if (value.length > 6) value = value.slice(0, 6);
  e.target.value = value;
});

codeForm.addEventListener("submit", function (event) {
  const accessCode = accessCodeInput.value;

  if (accessCode.length !== 6) {
    showMessage("O código deve ter exatamente 6 dígitos.", true);
    return;
  }

  showMessage("Código validado! Redirecionando...", false);
});

function showMessage(text, isError) {
  message.textContent = text;
  message.classList.remove("hidden");
  if (isError) {
    message.classList.add("text-red-600");
    message.classList.remove("text-green-600");
  } else {
    message.classList.add("text-green-600");
    message.classList.remove("text-red-600");
  }
}