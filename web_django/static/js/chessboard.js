function closeModalWindow(modal){
    modal.style = {'visibility': 'hidden'};
}

function showGiveUpModal(){
    $('#give_up_modal').css({'visibility': 'visible'});
}

function showDrawOfferModal(){
    socket_connection.send(JSON.stringify({"type": "draw_offer"}));
    $('#draw_offer_create_modal').css({"visibility": 'visible'});
    draw_offer = true;
    console.log(draw_offer);
}

function giveUp(){
    socket_connection.send(JSON.stringify({"type": "give_up"}));
    $('#give_up_modal').css({"visibility": "hidden"});
}

function drawOfferAccept(){
    socket_connection.send(JSON.stringify({"type": "draw_offer"}));
    $('#draw_offer_modal').css({"visibility": "hidden"});
}

function transitionAcceptModal(url){
    replaceText(document.getElementById('transition_message'), 'Ты уверен что хочешь перейти на страницу ' + url + '?');
    $('#transition_modal').css({'visibility': 'visible'});
}

function transitionUser(url){
    window.location.href = url;
}

function webSocketConnector(){
    let game_tag = window.location.pathname.split('/').at(-2);

    let connect = new WebSocket('ws://127.0.0.1:8000/websocket/games/' + game_tag);

    return connect;
}

function fillData(user_id, board_fen, first_player_time, second_player_time, draw_offer, color, turn){
    updateUserId(user_id);
    updateBoardFEN(board_fen);
    updateFirstPlayerTime(first_player_time);
    updateSecondPlayerTime(second_player_time);
    updateDrawOffer(draw_offer);
    updateColor(color);
    updateTurn(turn);
}

function updateUserId(user_id_var){
    var user_id = user_id_var;
    window.user_id = user_id;
}

function updateBoardFEN(board_fen_var){
    var board_fen = board_fen_var;
    window.board_fen = board_fen;
}

function updateFirstPlayerTime(first_player_time_var){
    var first_player_time = first_player_time_var;
    window.first_player_time = first_player_time;
}

function updateSecondPlayerTime(second_player_time_var){
    var second_player_time = second_player_time_var;
    window.second_player_time = second_player_time;
}

function updateDrawOffer(draw_offer_var){
    var draw_offer = (draw_offer_var == "True");
    window.draw_offer = draw_offer;
}

function updateColor(color_var){
    var color = (color_var == "True");
    window.color = color;
}

function updateTurn(turn_var){
    var turn = (turn_var == "True");
    window.turn = turn;
}

function replaceText(element, text){
    if (element.innerText) {
        element.innerText = text;
    }

    else if (element.textContent) {
        element.textContent = text;
    }
}

function move(start_cell, end_cell){
    socket_connection.send(JSON.stringify({"type": "move", "start_cell": start_cell, "end_cell": end_cell}));
}


var socket_connection = webSocketConnector();


socket_connection.onmessage = function(event){
    let response = $.parseJSON(event.data);
    console.log(response);

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
        break;

    case "end_game":
        replaceText(document.getElementById('end_game_message'), response["message"]);
        $("#end_game_modal").css({"visibility": "visible"})
        break;

    case "on_check":
        $('#on_check_modal').css({"visibility": "visible"})
        break;

    case "update_board":
        // function
        break;
    }


}