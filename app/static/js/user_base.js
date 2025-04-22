const darkModeBtn = document.getElementById("dark_mode");
let currentState = false; // Default light mode

darkModeBtn.addEventListener("click", () => {
    currentState = !currentState; // Toggle state
    document.body.classList.toggle("dark", currentState);
    localStorage.setItem("darkMode", currentState); // Save preference
});

// Load saved mode on page reload
if (localStorage.getItem("darkMode") === "true") {
    document.body.classList.add("dark");
    currentState = true;
}