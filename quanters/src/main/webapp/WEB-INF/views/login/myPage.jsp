<%@ page language="java" contentType="text/html; charset=UTF-8"
         pageEncoding="UTF-8"%>
<script type="text/javascript" src="${pageContext.request.contextPath}/static/js/login/myPage.js"></script>
<p id="hiddenStockList">${stockList}</p>
<div class="d-flex justify-content-start" id="gridDiv">
    <div class="stockGrid">
        <div class="stockDiv">
            <p>서비스 제공 중인 주식 명단</p>
        </div>
        <table id="gridTable">
        </table>
    </div>
    <div class="stockGrid">
        <div class="stockDiv">
            <p>내가 추가한 주식 명단</p>
        </div>
        <table id="myGridTable">
        </table>
    </div>
</div>
<div class="d-flex justify-content-start" id="gridDiv">
    <div class="btnGridZone">
        <button id="gridBtn" class="btn btn-dark">추가</button>
    </div>
    <div class="btnGridZone">
        <button id="gridBtn2" class="btn btn-dark">삭제</button>
    </div>
</div>