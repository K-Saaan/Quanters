<%@ page language="java" contentType="text/html; charset=UTF-8"
         pageEncoding="UTF-8"%>
<script type="text/javascript" src="${pageContext.request.contextPath}/static/js/login/myPage.js"></script>
<p id="hiddenStockList">${stockList}</p>
<div class="d-flex justify-content-start" id="gridDiv">
    <div>
        <div class="stockTitle"><h3>현재 서비스 중 주가</h3></div>
        <div class="stockGrid" id="stockGrid">
        </div>
        <div class="stockGrid2" id="btnGrid">
            <button id="gridBtn" class="btn btn-dark">추가</button>
        </div>
    </div>
    <div>
        <div><h3 class="stockTitle">내가 추가한 주가</h3></div>
        <div class="stockGrid" id="stockGrid2">
        </div>
        <div class="stockGrid2" id="btnGrid2">
            <button id="gridBtn2" class="btn btn-dark">삭제</button>
        </div>
    </div>
    <div>
        <div><h3 class="stockTitle">현재 주가 현황</h3></div>
    </div>
</div>