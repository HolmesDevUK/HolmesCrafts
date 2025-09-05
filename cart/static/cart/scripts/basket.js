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

            sendAjax("/basket/update-ajax/", { item_id: itemId, quantity: newQty }, function(data) {
                subtotalCell.innerText = `£${data.subtotal}`;
                document.getElementById("order_total").innerText = `£${data.total}`;
            });
        });
    });

    // Handle item removal
    document.querySelectorAll('.removeButton').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const itemId = this.dataset.itemId;
            const row = this.closest('tr');

            sendAjax(`/basket/remove-ajax/${itemId}/`, null, function(data) {
                const tbody = document.querySelector(".basket_table tbody");
                const tfoot = document.querySelector(".basket_table tfoot");

                row.remove();

                if (data.total > 0) {
                document.getElementById("order_total").innerText = `£${data.total}`;
                } else {
                    tbody.innerHTML = '<tr><td colspan="6" id="empty_basket">The Basket is currently empty</td></tr>';
                    if (tfoot) tfoot.remove();
                }
            });

        });
    });

});