function startPrepareTimer(prepare_time_var){

    if (prepare_time_var <= 0) {
        clearPrepareDiv();
        return false;}

    var prepare_time_timer = window.setInterval(function(){
        if (prepare_time <= 0) {
            window.clearInterval(prepare_time_timer);
            clearPrepareDiv();
            startTimers();
            return false;}

        updatePrepareTime(window.prepare_time - 1);
    }, 1000);}


function clearPrepareDiv(){
    document.getElementById('prepare_time_div').remove();
}

startPrepareTimer(prepare_time)