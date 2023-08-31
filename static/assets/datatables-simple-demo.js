window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesAll = document.getElementById('datatables-all');
    if (datatablesAll) {
        new simpleDatatables.DataTable(datatablesAll);
    }

    const datatablesKeywords = document.getElementById('datatables-keywords');
    if (datatablesKeywords) {
        new simpleDatatables.DataTable(datatablesKeywords);
    }

    const datatablesCitations = document.getElementById('datatables-citations');
    if (datatablesCitations) {
        new simpleDatatables.DataTable(datatablesCitations);
    }
});
