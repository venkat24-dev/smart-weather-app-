const signInTab = document.getElementById('signInTab');
const signUpTab = document.getElementById('signUpTab');
const signInForm = document.getElementById('signInForm');
const signUpForm = document.getElementById('signUpForm');
const toSignUpLink = document.getElementById('toSignUp');
const toSignInLink = document.getElementById('toSignIn');

function showSignIn() {
    signInTab.classList.add('active');
    signUpTab.classList.remove('active');
    signInForm.classList.add('active');
    signUpForm.classList.remove('active');
}

function showSignUp() {
    signUpTab.classList.add('active');
    signInTab.classList.remove('active');
    signUpForm.classList.add('active');
    signInForm.classList.remove('active');
}

signInTab.addEventListener('click', showSignIn);
signUpTab.addEventListener('click', showSignUp);
toSignUpLink.addEventListener('click', showSignUp);
toSignInLink.addEventListener('click', showSignIn);

signInForm.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Sign In form submitted');
});

signUpForm.addEventListener('submit', (e) => {
    e.preventDefault();
    if (document.getElementById('signup-password').value !== document.getElementById('signup-confirm-password').value) {
        alert('Passwords do not match!');
        return;
    }
    alert('Sign Up form submitted');
});

