document.addEventListener('DOMContentLoaded', function () {
    //회원가입 버튼 이벤트
    $('#registerButton').on('click',function () {
        var reply = confirm("회원가입 하시겠습니까?");
        if(reply) {
            if($("#regId").val() == "") {
                alert("ID를 입력하세요.")
                return
            }
            if($("#regPwd").val() == "") {
                alert("PW를 입력하세요.")
                return
            }
            var regParam = {
                userId: $("#regId").val(),
                userPw: $("#regPwd").val(),
                userState: "ACTIVE"
            };
            postajax("/login/register", regParam, function (returnData) {
                if (returnData == 1) {
                    alert("등록이 완료됐습니다.");
                    window.location.href = "/home/search";
                    // $("#couponSearch", opener.document).trigger("click");
                    // window.close();
                } else {
                    alert("register fail!");
                }
            })
        }
    });
});