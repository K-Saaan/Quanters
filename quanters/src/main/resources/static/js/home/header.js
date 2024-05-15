document.addEventListener('DOMContentLoaded', function () {
    var userId = $("#userId").text();
    // 로그인이 되어있으면
    if(userId != "") {
        $("#loginButton").text("Logout")
        $("#loginHref").attr("href", "/login/logout")
        $("#homepageHref").attr("href", "/home/search")
        $("#loginMenu1").show()
        $("#loginMenu3").show()
    } else {
        $("#loginButton").text("Login/Register")
        $("#loginHref").attr("href", "/login/loginPage")
        $("#homepageHref").attr("href", "/home/home")
        $("#loginMenu1").hide()
        $("#loginMenu3").hide()
    }
});