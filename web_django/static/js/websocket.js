function webSocketConnector(){

    let game_tag = window.location.pathname.split('/').at(-2);

    let connect = new WebSocket('ws://chess-kb.ru/websocket/games/' + game_tag);

    return connect;
}


function onMessage(event){
    let response = $.parseJSON(event.data);

    switch(response["event"]){

    case "draw_offer":
        if (Number(response["recipient"]) == user_id){
            if(!draw_offer){
                $('#draw_offer_modal').css({"visibility": "visible"})}
            }
        break;

    case "illegal_move_error":
        replaceText(document.getElementById('illegal_move_message'), response["message"]);
        $("#illegal_move_modal").css({"visibility": "visible"})
        window.c.updateMatrixPosition(window.board_fen)
        break;

    case "end_game":
        replaceText(document.getElementById('end_game_message'), response["message"]);
        $("#end_game_modal").css({"visibility": "visible"})
        window.clearInterval(window.chessTimer);
        break;

    case "on_check":
        if (response["recipient"] == user_id){
            $('#on_check_modal').css({"visibility": "visible"})
        }

        break;

    case "update_board":
        window.c.updateMatrixPosition(response["board"]);
        window.board_fen = response["board"];

        window.onMoveSound();

        if (window.turn){
            updateTurn("false");
        }
        else {updateTurn("true");}

        updateFirstPlayerTime(response["first_user_time"]);
        updateSecondPlayerTime(response["second_user_time"]);
        break;
        }
    }

function move(start_cell, end_cell){

    socket_connection.send(JSON.stringify({
    "type": "move", "start_cell": start_cell.getElementsByClassName('squareNotation')[0].innerText,
    "end_cell": end_cell.getElementsByClassName('squareNotation')[0].innerText}));
}


var socket_connection = webSocketConnector();

socket_connection.onmessage = onMessage;