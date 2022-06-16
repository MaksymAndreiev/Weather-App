// $('#input-city').attr("disabled", 'disabled');
$("#login").click(function () {
    $('#input-city').attr("disabled", 'disabled');
    $(this).animate({
        width: "250px",
        height: "250px"
    }, 800);
    $("#field").animate({
        opacity: "1",
        top: 55
    }, 800);
    $(".fas").animate({
        opacity: "0"
    }, 800);
});

$('#enter').click(function () {
    $("#input-city").attr("disabled", false);
    $("#login").animate({
        width: "50px",
        height: "50px"
    }, 800);
    $("#field").animate({
        opacity: "0",
        top: 0
    }, 800);
    $(".fas").animate({
        opacity: "1"
    }, 800);
});
