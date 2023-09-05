function check_token(){

        var token = $("#token").val();

        if (token.length < 35){

            $("label").replaceWith("<label for=\"token\" id=\"class=label_for_token\" style=\"color: red;\">Длина токена слишком маленькая! ⚠</label>");
            return false;

        }

        $.ajax(
        {
        type: 'POST',
        url: `http://192.168.1.60:8000/api/v1/authorize?token=${token}`,
        success: function(data){
            var response = $.parseJSON(data);

            if (!response.success){
                $("label").replaceWith(("<label for=\"token\" id=\"class=label_for_token\" style=\"color: red;\">Такого токена не существует! ⚠</label>"));
                return false;
            }
        location.reload(true);
            }
        });
    };
