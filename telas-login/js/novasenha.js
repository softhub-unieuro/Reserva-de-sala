const newPasswordInput = document.getElementById("newPassword");
const confirmPasswordInput = document.getElementById("confirmPassword");
const form = document.getElementById("newPasswordForm");
const errorMessage = document.getElementById("errorMessage");

const reqLength = document.getElementById("req-length");
const reqUpper = document.getElementById("req-upper");
const reqLower = document.getElementById("req-lower");
const reqNumber = document.getElementById("req-number");
const reqSpecial = document.getElementById("req-special");

const requirements = [
  { el: reqLength, regex: /.{8,}/ },
  { el: reqUpper, regex: /[A-Z]/ },
  { el: reqLower, regex: /[a-z]/ },
  { el: reqNumber, regex: /[0-9]/ },
  { el: reqSpecial, regex: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/ },
];

function updateRequirementCheckboxes() {
  const password = newPasswordInput.value;
  requirements.forEach((req) => {
    const isMet = req.regex.test(password);
    req.el.checked = isMet;
    if (isMet) {
      req.el.classList.remove("text-gray-400");
      req.el.classList.add("text-green-600");
    } else {
      req.el.classList.remove("text-green-600");
      req.el.classList.add("text-gray-400");
    }
  });
}

newPasswordInput.addEventListener("input", () => {
  errorMessage.textContent = "";
  updateRequirementCheckboxes();
});

form.addEventListener("submit", function (event) {
  event.preventDefault();
  errorMessage.textContent = "";
  errorMessage.classList.remove("text-green-600", "text-red-600");

  const newPassword = newPasswordInput.value;
  const confirmPassword = confirmPasswordInput.value;
  const allRequirementsMet = requirements.every((req) => req.el.checked);

  if (!allRequirementsMet) {
    errorMessage.textContent = "A senha não atende a todos os requisitos.";
    errorMessage.classList.add("text-red-600");
    return;
  }

  if (newPassword !== confirmPassword) {
    errorMessage.textContent = "As senhas não conferem.";
    errorMessage.classList.add("text-red-600");
    return;
  }

  errorMessage.textContent = "Senha redefinida! Redirecionando para o login...";
  errorMessage.classList.add("text-green-600");

  newPasswordInput.disabled = true;
  confirmPasswordInput.disabled = true;
  form.querySelector("button").disabled = true;

  setTimeout(() => {
    window.location.href = "login.html";
  }, 1500);
});

updateRequirementCheckboxes();
