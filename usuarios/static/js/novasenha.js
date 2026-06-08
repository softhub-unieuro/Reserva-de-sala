document.addEventListener("DOMContentLoaded", () => {
  const passwordInput = document.getElementById("newPassword");
  const confirmInput = document.getElementById("confirmPassword");
  const form = document.getElementById("newPasswordForm");
  const errorMessage = document.getElementById("errorMessage");

  // Checkboxes dos requisitos
  const reqLength = document.getElementById("req-length");
  const reqUpper = document.getElementById("req-upper");
  const reqLower = document.getElementById("req-lower");
  const reqNumber = document.getElementById("req-number");
  const reqSpecial = document.getElementById("req-special");

  // Função para validar senha
  function validatePassword(password) {
    return {
      length: password.length >= 8,
      upper: /[A-Z]/.test(password),
      lower: /[a-z]/.test(password),
      number: /\d/.test(password),
      special: /[!@#$%^&*(),.?":{}|<>]/.test(password),
    };
  }

  // Atualiza o estado dos requisitos visualmente
  function updateRequirements(password) {
    const validity = validatePassword(password);

    reqLength.checked = validity.length;
    reqUpper.checked = validity.upper;
    reqLower.checked = validity.lower;
    reqNumber.checked = validity.number;
    reqSpecial.checked = validity.special;

    // Troca a cor dos checkboxes conforme o estado
    document.querySelectorAll(".req-checkbox").forEach((checkbox) => {
      if (checkbox.checked) {
        checkbox.classList.add("text-green-500");
        checkbox.classList.remove("text-gray-400");
      } else {
        checkbox.classList.add("text-gray-400");
        checkbox.classList.remove("text-green-500");
      }
    });
  }

  // Validação em tempo real da senha
  passwordInput.addEventListener("input", (e) => {
    const password = e.target.value;
    updateRequirements(password);
  });

  // Verifica se as senhas coincidem
  confirmInput.addEventListener("input", () => {
    if (confirmInput.value && confirmInput.value !== passwordInput.value) {
      errorMessage.textContent = "As senhas não coincidem.";
      errorMessage.classList.add("text-red-600");
      errorMessage.classList.remove("text-green-600");
    } else if (confirmInput.value === passwordInput.value && confirmInput.value !== "") {
      errorMessage.textContent = "As senhas coincidem!";
      errorMessage.classList.add("text-green-600");
      errorMessage.classList.remove("text-red-600");
    } else {
      errorMessage.textContent = "";
    }
  });

  // Impede envio se a senha não for válida
  form.addEventListener("submit", (e) => {
    const password = passwordInput.value;
    const confirm = confirmInput.value;
    const validity = validatePassword(password);

    if (
      !validity.length ||
      !validity.upper ||
      !validity.lower ||
      !validity.number ||
      !validity.special
    ) {
      e.preventDefault();
      errorMessage.textContent = "A senha não atende a todos os requisitos.";
      errorMessage.classList.add("text-red-600");
      return;
    }

    if (password !== confirm) {
      e.preventDefault();
      errorMessage.textContent = "As senhas não coincidem.";
      errorMessage.classList.add("text-red-600");
      return;
    }

    // Tudo certo
    errorMessage.textContent = "";
  });
});
