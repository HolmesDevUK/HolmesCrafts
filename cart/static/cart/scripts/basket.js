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
                document.getElementById("cartNumber").innerText = data.total_quantity;
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
                const checkout = document.querySelector(".checkout");

                row.remove();
                document.getElementById("cartNumber").innerText = data.total_quantity;
                console.log("AJAX response:", data);

                if (data.total > 0) {
                document.getElementById("order_total").innerText = `£${data.total}`;
                } else {
                    tbody.innerHTML = '<tr><td colspan="6" id="empty_basket">The Basket is currently empty</td></tr>';
                    if (tfoot) tfoot.remove();
                    if (checkout) checkout.remove();
                }
            });

        });
    });

});


document.addEventListener("DOMContentLoaded", function () {
    const checkoutForm = document.getElementById("checkout-form");
    const checkoutButton = document.getElementById("checkout-btn");

    if (checkoutForm) {
        checkoutForm.addEventListener("submit", function (e) {
            e.preventDefault(); // stop normal form submit

            const formData = new FormData(checkoutForm);

            fetch("/checkout/create-session/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                },
                body: formData,
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                if (data.sessionId) {
                    const stripe = Stripe("{{ STRIPE_PK }}"); // pass this via template context
                    return stripe.redirectToCheckout({ sessionId: data.sessionId });
                } else {
                    alert("Something went wrong starting checkout.");
                }
            })
            .catch(error => {
                console.error("Checkout error:", error);
                alert("There was an error. Please try again.");
            });
        });
    }
});

