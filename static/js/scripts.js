// 
// Scripts

let monBouton = document.getElementById("btnSearchDoi");
if (monBouton != null) {
    // Ajoute un événement de clic au bouton
    monBouton.onclick = function() {
        // Récupère l'élément HTML de l'input
        let input = document.getElementById("searchInputDOI");

        // Récupère le contenu de l'input
        let contenuInput = input.value;
        let resultat = document.getElementById("result-doi-text");

        // Construit le lien avec le paramètre de recherche
        let lienRequete = "/doi-get-data?q=" + encodeURIComponent(contenuInput);

        // Requête AJAX
        setTimeout(function() {
            fetch(lienRequete)
                .then(response => response.json())
                .then(data => {
                    resultat.innerHTML = JSON.stringify(data, null, 2);
                    // console.log(data);
        });
        }, 1500);
    };
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
