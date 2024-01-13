function webSocketConnector(){

    let game_tag = window.location.pathname.split('/').at(-2);

    let connect = new WebSocket(`${config.ssl_ws}://${config.domain}/websocket/games/` + game_tag + "/");

    return connect;
}


function onMessage(event){
    let response = $.parseJSON(event.data);

    switch(response["event"]){

    case "end_game":
        replaceText(document.getElementById('end_game_message'), response["message"]);
        $("#end_game_modal").css({"visibility": "visible"})
        window.clearInterval(window.chessTimer);
        break;

    case "update_board":
        window.c.updateMatrixPosition(response["board"]);
        window.board_fen = response["board"];
        if (window.turn){
            updateTurn("false");
        }
        else {updateTurn("true");}

        updateFirstPlayerTime(response["first_user_time"]);
        updateSecondPlayerTime(response["second_user_time"]);
        break;
        }
    }

var socket_connection = webSocketConnector();

function timeEnd(){
    socket_connection.send(JSON.stringify({"type": "end_timer"}))
}



socket_connection.onmessage = onMessage;