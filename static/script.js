document.addEventListener("DOMContentLoaded", function() {

    document.getElementById("startButton").addEventListener("click", function(event) {
        event.preventDefault(); 
        document.getElementById("authSection").classList.remove("hidden");
        document.getElementById("authSection").scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        document.body.style.backgroundImage = "none";
        document.body.style.backgroundColor = "#000000";
    });
});
