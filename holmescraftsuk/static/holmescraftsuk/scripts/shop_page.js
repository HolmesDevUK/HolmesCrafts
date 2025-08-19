
function changeImg()
{

	var shopImg = document.getElementById("shop_img");

	if(event.target.src != null)
	{
		shopImg.setAttribute("src", event.target.src);
	}

}

function colorVar(Img, color, name, code)
{

	var checkoutForm = document.getElementById("card_var_form");
	var quantityLabel = document.getElementById("card_var_quantity");
	var smallImg = document.getElementById("small_img");
	var shopImg = document.getElementById("shop_img");
	var colorVarBtn = document.getElementById("color_var_btn");
	var formName = document.getElementById("card_var_name")
	var formImg = document.getElementById("card_var_img")
	var formCode = document.getElementById("card_var_code")

	smallImg.setAttribute("src", Img);
	shopImg.setAttribute("src", Img);
	quantityLabel.classList.remove("hidden")
	checkoutForm.classList.remove("hidden")
	checkoutForm.setAttribute("class", "add_to_cart_form")
	formImg.setAttribute("value", Img)
	formName.setAttribute("value", name + " (" + color + ")")
	formCode.setAttribute("value", code + " (" + color + ")")

	colorVarBtn.innerHTML = color;

	console.log("works")

}