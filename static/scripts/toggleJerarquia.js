const tipoSelect = document.getElementById('id_tipo');
    const jerarquiaDiv = document.getElementById('id_jerarquia_acoso').closest('.mb-3');

    function toggleJerarquia() {
        if (tipoSelect.value === "ACL") {
            jerarquiaDiv.style.display = 'block';
        } else {
            jerarquiaDiv.style.display = 'none';
            document.getElementById('id_jerarquia_acoso').value = '';
        }
    }

    tipoSelect.addEventListener('change', toggleJerarquia);
    toggleJerarquia();