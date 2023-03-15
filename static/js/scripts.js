// 
// Scripts
// 

var monBouton = document.getElementById("btnSearchDoi");

// Ajoute un événement de clic au bouton
monBouton.onclick = function() {
    // Récupère l'élément HTML de l'input
    var input = document.getElementById("searchInputDOI");

    // Récupère le contenu de l'input
    var contenuInput = input.value;

    // Construit le lien avec le paramètre de recherche
    var lienRequete = "/doi-search?q=" + encodeURIComponent(contenuInput);
    // REVOIR
    setTimeout(function() {
        fetch('/doi-search')
        .then(response => response.json())
        .then(data => {
            console.log(data);
        });
    }, 1500);
};

function envoyerRequete() {



}

window.addEventListener('DOMContentLoaded', event => {
    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});
