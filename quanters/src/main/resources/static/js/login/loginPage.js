document.addEventListener('DOMContentLoaded', function () {

    $('#id').keypress(function(event) {
        if(event.keyCode == 13){
            login();
        }
    });

    $('#pwd').keypress(function(event) {
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
    if($("id").val() == "") {
        alert("아이디를 확인해주세요.");
        $("#id").focus();
        return;
    }

    if($("#pwd").val() == "") {
        alert("비밀번호를 확인해주세요.");
        $("#pwd").focus();
        return;
    }

    var param = new Object();
    param.text_id = $("#id").val();
    param.text_pwd = $("#pwd").val();

    postajax("/login/loginAction", param, function(returnData){
        console.log(returnData);
        if(returnData.RESULT == "GO_MAIN"){
            // goMainPage(returnData.URL);
            window.location.href = "/home/search";
        }else if(returnData.RESULT == "INPUT_NULL"){
            alert("아이디 또는 비밀번호를 입력해주세요.");
        }else if(returnData.RESULT == "LOGIN_FAIL"){
            alert("없는 계정입니다.");
        }else if(returnData.RESULT == "PWD_FAIL"){
            alert("비밀번호가 일치하지 않습니다." + returnData.FAILCNT);
        }else if(returnData.RESULT == "OVER_LOGIN_FAIL_CNT"){
            alert("로그인 실패 횟수를 초과했습니다. 관리자에게 문의하세요.");
        }else if(returnData.RESULT == "OVER_PASSWORD_DUE_DATE"){
            alert("비밀번호 만료일입니다. 비밀번호를 재설정해주세요.");
        }else if(returnData.RESULT == "LOCK_ACCOUNT"){
            alert("계정이 잠겼습니다. 관리자에게 문의하세요.");
        }
    });
}