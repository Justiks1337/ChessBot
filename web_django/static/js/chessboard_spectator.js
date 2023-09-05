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

function webSocketConnector(){
    let game_tag = window.location.pathname.split('/').at(-2);

    let connect = new WebSocket('ws://192.168.1.60:8000/websocket/games/' + game_tag);

    return connect;
}

function fillData(board_fen, first_player_time, second_player_time){
    updateBoardFEN(board_fen);
    updateFirstPlayerTime(first_player_time);
    updateSecondPlayerTime(second_player_time);
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

function replaceText(element, text){
    if (element.innerText) {
        element.innerText = text;
    }

    else if (element.textContent) {
        element.textContent = text;
    }
}

var socket_connection = webSocketConnector();

socket_connection.onmessage = function(event){
    let response = $.parseJSON(event.data);

    switch(response["event"]){

    case "end_game":
        replaceText(document.getElementById('end_game_message'), response["message"]);
        $("#end_game_modal").css({"visibility": "visible"})
        break;

    case "update_board":
        window.c.updateMatrixPosition(response["board"]);
        window.board_fen = response["board"];
        break;
    }
}