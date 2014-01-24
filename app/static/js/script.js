$('a.audio_play').click(function() {
    var progressBar = $(this).next('div.progress_bar');
    var duration = progressBar.attr('data');
    progressBar.attr("style", "-webkit-transition: width " + duration + "s linear !important");
    // Add transition for non-webkit browsers

    if (this.firstChild.paused === false) {
        this.firstChild.pause();
        $(this).children('div.play_btn').children('span.glyphicon')
            .attr('class', 'glyphicon glyphicon-play');
    } else {
        this.firstChild.play();
        progressBar.toggleClass('play');
        $(this).children('div.play_btn').children('span.glyphicon')
            .attr('class', 'glyphicon glyphicon-pause');
    }
});
