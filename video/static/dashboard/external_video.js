var videoAreaStatus = false;
var videoEditArea = $('#video-edit-area');

$(document).ready(function () {
    $('#open-add-video-btn').click(function () {
        if (!videoAreaStatus) {
            $('form').show();
            videoAreaStatus = true;
        } else {
            $('form').hide();
            videoAreaStatus = false;
        }
    });
});