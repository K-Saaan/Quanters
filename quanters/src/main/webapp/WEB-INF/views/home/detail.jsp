<%@ page language="java" contentType="text/html; charset=UTF-8"
         pageEncoding="UTF-8"%>
<script type="text/javascript" src="${pageContext.request.contextPath}/static/js/home/detail.js"></script>
<div class="outerDiv justify-content-center">
    <div class="d-flex justify-content-center searchBarDiv">
        <div class="searchBar d-flex justify-content-end align-items-md-center">
            <input type="text" id="searchText" autocomplete="off">
            <button id="searchBtn"><img src="${pageContext.request.contextPath}/static/image/search.png" class="searchImage"></button>
        </div>
    </div>
    <div class="d-flex justify-content-center searchUlDiv">
        <div class="autoComplete d-flex justify-content-end align-items-md-center">
            <ul class="searchUl">
            </ul>
        </div>
    </div>
    <div class="d-flex justify-content-center predictDiv">
        <span class="keyword">${keyword}</span>
        <span class="keywordStr">금일 주가 예측 결과</span>
        <span class="predictResult">${result}</span>
    </div>
</div>