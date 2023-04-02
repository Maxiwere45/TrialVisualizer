window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    let datatablesSimple = document.querySelectorAll('.datatablesSimple');
    if (datatablesSimple) {
        datatablesSimple.forEach(function(table) {
            new simpleDatatables.DataTable(table);
        });
    }
});
