document.addEventListener('DOMContentLoaded', function () {
    var userId = $("#userId").text();
    // 로그인이 되어있으면
    if(userId != "") {
        $("#loginButton").text("Logout")
        $("#loginHref").attr("href", "/login/logout")
        $("#loginMenu1").show()
        $("#loginMenu3").show()
    } else {
        $("#loginButton").text("Login/Register")
        $("#loginHref").attr("href", "/login/loginPage")
        $("#loginMenu1").hide()
        $("#loginMenu3").hide()
    }
});