
function changeImg()
{

	var shopImg = document.getElementById("shop_img");

	if(event.target.src != null)
	{
		shopImg.setAttribute("src", event.target.src);
	}

}

function colorVar(Img, color)
{
	var smallImg = document.getElementById("small_img");
	var shopImg = document.getElementById("shop_img");
	var colorVarBtn = document.getElementById("color_var_btn");
	var addToCartForm = document.getElementById("add_to_cart_form");
	var chosen_image_field = document.getElementById("chosen_image");

	smallImg.setAttribute("src", Img);
	shopImg.setAttribute("src", Img);

	colorVarBtn.innerHTML = color;

	addToCartForm.classList.remove('hidden');
	chosen_image_field.value = Img

	console.log("works")

}