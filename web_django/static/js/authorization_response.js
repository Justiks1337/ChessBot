$(document).ready(function() {

    $("#callback_form").submit(function() { return false; });

	$("#callback_send").on("click", function(event){
	    event.preventDefault();

        var token = $("#token").val();

        if (token.length < 35){

            $("label").replaceWith("<label for=\"token\" id=\"class=label_for_token\" style=\"color: red;\">Длина токена слишком маленькая! ⚠</label>");
            return false;

        }


        $.ajax(
        {
        type: 'POST',
        url: `http://127.0.0.1:8000/api/v1/authorize?token=${token}`,
        success: function(data){
            var response = $.parseJSON(data);

            if (!response.success){
                $("label").replaceWith(("<label for=\"token\" id=\"class=label_for_token\" style=\"color: red;\">Такого токена не существует! ⚠</label>"));
                return;
            }

            location.reload(true);
            }
        });
    });
})