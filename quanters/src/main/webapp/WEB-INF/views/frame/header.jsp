<script type="text/javascript" src="${pageContext.request.contextPath}/static/js/home/header.js"></script>
<div class="d-flex justify-content-center siteHeader">
    <div>
        <a id="homepageHref" href="${pageContext.request.contextPath}/home/home">
            <img src="${pageContext.request.contextPath}/static/image/logo.png" class="searchImage">
        </a>
    </div>
</div>
<div class="d-flex siteMenu">
    <div class="d-flex siteMenu3">
        <div class="loginMenu" id="loginMenu1" style="border: 1px solid black;padding: 10px; border-radius: 10px;">
            <p id="userId" style="margin: 0 auto; color: black;">${userId}</p>
        </div>
        <div class="loginMenu" id="loginMenu3" style="border: 1px solid black;padding: 10px; border-radius: 10px;">
            <a id="myPageHref" href="${pageContext.request.contextPath}/login/myPage">
                <p id="myPageButton" style="margin: 0 auto; color: black;">myPage</p>
            </a>
        </div>
        <div class="loginMenu" id="loginMenu2" style="border: 1px solid black;padding: 10px; border-radius: 10px;">
            <a id="loginHref" href="${pageContext.request.contextPath}/login/loginPage">
                <p id="loginButton" style="margin: 0 auto; color: black;">Login/Register</p>
            </a>
        </div>
    </div>
</div>