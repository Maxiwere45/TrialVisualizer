// Récupération de l'élément de formulaire
let inputFile = document.getElementById('file');

// Ajout d'un gestionnaire d'événement pour le changement de fichier
inputFile.addEventListener('change', function() {
  // Récupération du nom du fichier
  let fileName = this.files[0].name;

  // Affichage du nom du fichier dans la console
  console.log(fileName);
});
