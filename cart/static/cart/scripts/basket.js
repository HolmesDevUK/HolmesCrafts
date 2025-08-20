var productTotalsCell = document.getElementsByClassName("totals");
var productPrices = document.getElementsByClassName("basket_price");
var productQuantities = document.getElementsByClassName("quantity");
var total;
var orderTotal = 0;
var orderTotalCell = document.getElementById("order_total");



function calc_product_totals() {
    
    for(i=0; i<productQuantities.length; i++) {
        total = parseFloat(productPrices[i].innerHTML) * parseFloat(productQuantities[i].innerHTML);
        console.log(orderTotal);
        orderTotal += total;
        console.log(total);
        console.log(orderTotal);
        productTotalsCell[i].innerHTML = "£" + total.toFixed(2);
        productPrices[i].innerHTML = "£" + productPrices[i].innerHTML;
    }

    orderTotalCell.innerHTML = "£" + orderTotal.toFixed(2);
}


function basketLoad() {
    calc_product_totals();
}

basketLoad();
    