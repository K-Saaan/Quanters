<%@ page language="java" contentType="text/html; charset=UTF-8"
         pageEncoding="UTF-8"%>
<script type="text/javascript" src="${pageContext.request.contextPath}/static/js/login/myPage.js"></script>
<p id="hiddenStockList">${stockList}</p>
<div class="d-flex justify-content-start" id="gridLargeDiv2">
    <div class="gridBigDiv2">
        <div><h3 class="stockTitle">현재 주가 현황</h3></div>
        <div class="stockGrid3">
            <div id="stockGraph" style="height: 100%;"></div>
        </div>
    </div>
</div>
<div class="d-flex justify-content-start" id="gridLargeDiv1">
    <div class="gridBigDiv1">
        <div class="stockTitle">
            <div>
                <h3>현재 서비스 중 주가</h3>
            </div>
            <div>
                <button id="gridBtn" class="btn btn-dark">추가</button></div>
            </div>
        <div class="stockGrid" id="stockGrid">
        </div>
    </div>
    <div class="gridBigDiv1">
        <div class="stockTitle">
            <div>
                <h3>내가 추가한 주가</h3>
            </div>
            <div>
                <button id="gridBtn2" class="btn btn-dark">삭제</button></div>
            </div>
        <div class="stockGrid" id="stockGrid2">
        </div>
    </div>
    <div class="gridBigDiv1">
        <div class="stockTitle2">
            <div>
                <h3>해당 주가 예측</h3>
            </div>
            <div class="predictGrid">
                <img src="${pageContext.request.contextPath}/static/image/up.png" class="searchImage" id="upImage">
                <img src="${pageContext.request.contextPath}/static/image/down.png" class="searchImage" id="downImage">
            </div>
        </div>
    </div>
    <div class="gridBigDiv1">
        <div class="stockTitle2">
            <div>
                <h3>전날 대비 증감</h3>
            </div>
            <div class="">
                <p id="priceDiff"></p>
            </div>
        </div>
    </div>
</div>