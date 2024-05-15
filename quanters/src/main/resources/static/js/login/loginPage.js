document.addEventListener('DOMContentLoaded', function () {
    var errorMessage = $('#errorMessage').text();
    if (errorMessage != "") {
        alert(errorMessage)
    }

    $('#username').keypress(function(event) {
        if(event.keyCode == 13){
            login();
        }
    });

    $('#password').keypress(function(event) {
        if(event.keyCode == 13){
            login();
        }
    });

    //로그인 버튼 이벤트
    $('#loginBtn').on('click',function () {
        login();
    });
    //회원가입 버튼 이벤트
    $('#registerBtn').on('click',function () {
        window.location.href = "/login/registerPage";
    });

});


function login(){
    if($("username").val() == "") {
        alert("아이디를 확인해주세요.");
        $("#username").focus();
        return;
    }

    if($("#password").val() == "") {
        alert("비밀번호를 확인해주세요.");
        $("#password").focus();
        return;
    }

    var form = document.loginForm;
    form.username = $("username").val();
    form.password = $("password").val();
    form.submit();

    // var param = new Object();
    // param.username = $("#username").val();
    // param.password = $("#password").val();

    // const param = {
    //     username: $("#username").val(), password: $("#password").val()
    // }
    //
    // loginPostajax("/login/loginAction", param, function(returnData){
    //     console.log("loginPage js 에서 로그인 성공")
    //     window.location.href = "/home/home";
    // });
}