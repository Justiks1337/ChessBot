var chessTimer;

function updateFirstPlayerTime(first_player_time_var){

    var first_player_time = first_player_time_var;
    window.first_player_time = first_player_time;
    updateTimer(first_player_time, "first_player_time");
}

function updateSecondPlayerTime(second_player_time_var){

    var second_player_time = second_player_time_var;
    window.second_player_time = second_player_time;
    updateTimer(second_player_time, "second_player_time");

    if (first_player_time <= 0){
        clearInterval(chessTimer);
    }
}

function startTimers(){
    chessTimer = setInterval(function () {
        if (window.turn){
            updateFirstPlayerTime(window.first_player_time - 1);
            return;
        }
            updateSecondPlayerTime(window.second_player_time - 1);
    }, 1000);}

function updateTimer(time, player){

    ifNegativeTime(time);

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

function ifNegativeTime(player_time){
    if (player_time < 0) {

        string = window.location.pathname.slice(0, -1);

        tag = string.slice(string.lastIndexOf('/')+1);

        console.log(tag);

        $.ajax(
        {
        type: 'POST',
        url: `https://chess-kb.ru/api/v1/check_timer?tag=${tag}`
        });
    }
}
