<%@ page language="java" contentType="text/html; charset=UTF-8"
         pageEncoding="UTF-8"%>
<script type="text/javascript" src="${pageContext.request.contextPath}/static/js/login/registerPage.js"></script>
<div class="d-flex justify-content-center">
    <div class="loginDiv">
        <main class="form-signin">
            <form action="registerPage.jsp" method="post">
                <div class="form-floating">
                    <label for="regId">ID</label>
                    <input type="text" class="form-control" id="regId" placeholder="아이디 입력...">
                </div>
                <div class="form-floating" style="margin-top: 10px;">
                    <label for="regPwd">PW</label>
                    <input type="password" class="form-control" id="regPwd" placeholder="Password">
                </div>
                <button type="button" class="btn btn-outline-dark loginBtn" id="registerButton">회원가입</button>
            </form>
        </main>
    </div>
</div>