document.addEventListener('DOMContentLoaded', function() {

    // Prevent form submissions from reloading the page
    document.querySelectorAll('.quantity-form').forEach(form => {
        form.addEventListener('submit', e => e.preventDefault());
    });

    // Handle quantity change
    document.querySelectorAll('.quantity_input').forEach(input => {
        input.addEventListener('change', function() {
            const itemId = this.dataset.itemId;
            const newQty = this.value;
            const row = this.closest('tr');
            const subtotalCell = row.querySelector('.totals');

            fetch("/basket/update-ajax/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ 'item_id': itemId, 'quantity': newQty })
            })
            .then(response => {
                if (!response.ok) throw new Error('Network error');
                return response.json();
            })
            .then(data => {
                subtotalCell.innerText = `£${data.subtotal}`;
                document.getElementById('order_total').innerText = `£${data.total}`;
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Handle item removal
    document.querySelectorAll('.removeButton').forEach(button => {
        button.addEventListener('click', function() {
            e.preventDefault();
            const itemId = this.dataset.itemId;
            const row = this.closest('tr');

            fetch(`/basket/remove-ajax/${itemId}/`, {
                method: 'POST',
                headers: { 
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                 }
            })
            .then(response => {
                if (!response.ok) throw new Error('Network error');
                return response.json();
            })
            .then(data => {
                row.remove();
                document.getElementById('order_total').innerText = `£${data.total}`;

                if (data.total == 0) {
                    const tbody = document.querySelector('.basket_table tbody');
                    tbody.innerHTML = '<tr><td colspan="6" id="empty_basket">The Basket is currently empty</td></tr>';
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
