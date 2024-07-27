document.addEventListener('DOMContentLoaded', function() {
    const selects = document.querySelectorAll('.form-group select');

    selects.forEach(select => {
        select.addEventListener('change', function() {
            const value = this.value;
            if (value === 'Yes') {
                this.style.borderColor = '#28a745'; // Green border for 'Yes'
            } else if (value === 'No') {
                this.style.borderColor = '#c32f2f'; // Red border for 'No'
            } else {
                this.style.borderColor = '#ccc'; // Default border color
            }
        });
    });
});
