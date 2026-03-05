document.addEventListener('DOMContentLoaded', function() {
        const personaSelect = document.getElementById('id_persona');
        const nombreInput = document.getElementById('id_nombre');

        if (personaSelect && nombreInput) {
            personaSelect.addEventListener('change', function() {
                const selectedOption = this.options[this.selectedIndex];

                if (selectedOption && selectedOption.value) {
                    nombreInput.value = selectedOption.text;
                }
            });
        }
    });