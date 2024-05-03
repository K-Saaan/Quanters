<%@ page language="java" contentType="text/html; charset=UTF-8"
         pageEncoding="UTF-8"%>
<script type="text/javascript" src="${pageContext.request.contextPath}/static/js/login/loginPage.js"></script>
<div class="d-flex justify-content-center">
    <div class="loginDiv">
        <main class="form-signin">
            <form action="loginPage.jsp" method="post">
                <div class="form-floating">
                    <label for="id">ID</label>
                    <input type="text" class="form-control" id="id" placeholder="아이디 입력...">
                </div>
                <div class="form-floating" style="margin-top: 10px;">
                    <label for="pwd">PW</label>
                    <input type="password" class="form-control" id="pwd" placeholder="Password">
                </div>
                <button type="button" class="btn btn-outline-dark loginBtn" id="loginBtn">로그인</button>
                <button type="button" class="btn btn-outline-dark loginBtn" id="registerBtn">회원가입</button>
            </form>
        </main>
    </div>
</div>