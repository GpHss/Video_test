$(document).ready(function () {
    $('.update-btn').click(function () {
        var inputId = $('#sub_id');
        var inputNumber = $('#number');
        var inputUrl = $('#url');

        var videosubId = parseInt($(this).attr('data-id'));
        var videoNumber = parseInt($(this).attr('data-number'));
        var videoUrl = $(this).attr('data-url');

        inputId.val(videosubId);
        inputNumber.val(videoNumber);
        inputUrl.val(videoUrl);
    });
});