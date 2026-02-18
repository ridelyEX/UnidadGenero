function search_by_name() {
    let input = document.getElementById('searchBar').value
    input = input.toLowerCase();
    let x = document.querySelectorAll('tbody tr.name');
    for (i = 0; i < x.length; i++) {
        let nombre = x[i].querySelector('td:first-child').textContent.toLowerCase();

        if (nombre.includes(input)) {
            x[i].style.display = '';
            console.log('ola');
        } else {
            x[i].style.display = 'none';
            console.log('ola2');
        }
    }
}