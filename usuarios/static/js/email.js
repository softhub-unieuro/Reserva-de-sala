const resetForm = document.getElementById("resetForm");
const emailInput = document.getElementById("email");
const message = document.getElementById("message");

resetForm.addEventListener("submit", function (event) {
  const email = emailInput.value;

  if (email === "") {
    showMessage("Insira o email para envio do código!", true);
    emailInput.classList.add("border-red-500", "focus:ring-red-500");
  } else {
    emailInput.classList.remove("border-red-500", "focus:ring-red-500");
    showMessage("E-mail enviado! Redirecionando...", false);
  }
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