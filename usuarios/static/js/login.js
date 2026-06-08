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

// Toggle password visibility
const togglePassword = document.getElementById('togglePassword');
const passwordInput = document.getElementById('password');
const eyeIcon = document.getElementById('eyeIcon');

if (togglePassword && passwordInput) {
    togglePassword.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        // Toggle icon
        if (type === 'text') {
            eyeIcon.classList.remove('fa-eye');
            eyeIcon.classList.add('fa-eye-slash');
        } else {
            eyeIcon.classList.remove('fa-eye-slash');
            eyeIcon.classList.add('fa-eye');
        }
    });
}