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

    let connect = new WebSocket('ws://192.168.1.60:8000/websocket/games/' + game_tag);

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

    console.log(first_player_time_var);

    var first_player_time = first_player_time_var;
    window.first_player_time = first_player_time;
    updateTimer(first_player_time, "first_player_time");
}

function updateSecondPlayerTime(second_player_time_var){

    console.log(second_player_time_var);

    var second_player_time = second_player_time_var;
    window.second_player_time = second_player_time;
    updateTimer(second_player_time, "second_player_time");
}

function updateDrawOffer(draw_offer_var){
    var draw_offer = (draw_offer_var.toLowerCase() == "true");
    window.draw_offer = draw_offer;
}

function updateColor(color_var){

    var color = (color_var.toLowerCase() == "true");
    var color_word;

    if (color) color_word = "w";
    else color_word = "b";

    window.color = color;
    window.color_word = color_word
}

function updateTurn(turn_var){
    var turn = (turn_var.toLowerCase() == "true");
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

function updateTimer(time, player){

    watch = Math.floor(time / 60) + ":" + (time % 60);

    replaceText($('#' + player)[0].children[0], watch);

}

function UpdateTimerFunction(){
    if (window.turn){
        updateFirstPlayerTime(window.first_player_time - 1);
        return;
    }
    updateSecondPlayerTime(window.second_player_time - 1);

}

function move(start_cell, end_cell){

    socket_connection.send(JSON.stringify({
    "type": "move", "start_cell": start_cell.getElementsByClassName('squareNotation')[0].innerText,
    "end_cell": end_cell.getElementsByClassName('squareNotation')[0].innerText}));
}

function possibles_to_move(piece_type){
    if (check_turn() && check_color(piece_type)) return true;
}

function check_turn(){
    if (window.turn == window.color) return true;
}

function check_color(piece_type){
    if (piece_type[0] == window.color_word) return true;
}

var socket_connection = webSocketConnector();
setInterval(function () {
    if (window.turn){
        updateFirstPlayerTime(window.first_player_time - 1);
        return;
    }
        updateSecondPlayerTime(window.second_player_time - 1);
}, 1000);

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
        window.c.updateMatrixPosition(window.board_fen)
        break;

    case "end_game":
        replaceText(document.getElementById('end_game_message'), response["message"]);
        $("#end_game_modal").css({"visibility": "visible"})
        break;

    case "on_check":
        if (response["recipient"] == user_id){
            $('#on_check_modal').css({"visibility": "visible"})
        }

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