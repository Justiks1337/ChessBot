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

function onMoveSound(){

    var on_move_sound = new Audio($("#on_move_sound").textContent);
    on_move_sound.play();
      }

function onReady(prepare_time, user_id, board_fen, first_player_time, second_player_time, draw_offer, color, turn){

    updatePrepareTime(prepare_time);
    updateUserId(user_id);
    updateBoardFEN(board_fen);
    updateFirstPlayerTime(first_player_time);
    updateSecondPlayerTime(second_player_time);
    updateDrawOffer(draw_offer);
    updateColor(color);
    updateTurn(turn);

    if (window.prepare_time <= 0){
        window.startTimers();
    }
}

function updatePrepareTime(prepare_time_var){
    var prepare_time = prepare_time_var;
    window.prepare_time = prepare_time;

    window.replaceText($("#prepare_counter")[0], prepare_time);
}

function updateUserId(user_id_var){
    var user_id = user_id_var;
    window.user_id = user_id;
}

function updateBoardFEN(board_fen_var){
    var board_fen = board_fen_var;
    window.board_fen = board_fen;
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

function possibles_to_move(piece_type){
    if (check_turn() && check_color(piece_type)) return true;
}

function check_turn(){
    if (window.turn == window.color) return true;
}

function check_color(piece_type){
    if (piece_type[0] == window.color_word) return true;
}

function showLegalMoves(legal_moves_array){
    legal_moves_array.forEach(function(element){
        $('#' + element)[0].offsetParent.append($('<div class="legal_move"></div>')[0]);
    })
}

function hideLegalMoves(){
    let legal_moves = [...document.getElementsByClassName("legal_move")];
    for (i=0; i < legal_moves.length; i++) {
        legal_moves[i].remove();
    }
}
