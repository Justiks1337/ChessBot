function closeModalWindow(modal){
    modal.style = {'visibility': 'hidden'};
}

function transitionAcceptModal(url){
    replaceText(document.getElementById('transition_message'), 'Ты уверен что хочешь перейти на страницу ' + url + '?');
    $('#transition_modal').css({'visibility': 'visible'});
}

function transitionUser(url){
    window.location.href = url;
}

function onReady(prepare_time, board_fen, first_player_time, second_player_time, turn){

    updatePrepareTime(prepare_time);
    updateBoardFEN(board_fen);
    updateFirstPlayerTime(first_player_time);
    updateSecondPlayerTime(second_player_time);
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

function updateBoardFEN(board_fen_var){
    var board_fen = board_fen_var;
    window.board_fen = board_fen;
}

function updateTurn(turn_var){
    var turn = (turn_var.toLowerCase() == "true");
    window.turn = turn;
}

