function getajax(paramUrl, paramData, returnCallBack, uiType){
	$.ajax({
		url:	paramUrl,
		method:	"GET",
		type:	"GET",
		data:	JSON.stringify(paramData),
		dataType:	"json",
		async:	true,
		contentType:	"application/json;charset=utf-8",
		cache:	false,
		success:	function(returnData){
			returnCallBack(returnData);
		},
		complete:	function(xhr, status){
		},
		error:	function(xhr, status, errorThrow){
		}
	});
}
function postajax(paramUrl, paramData, returnCallBack, uiType){
	$.ajax({
		url:	paramUrl,
		method:	"POST",
		type:	"POST",
		data:	JSON.stringify(paramData),
		dataType:	"json",
		async:	true,
		contentType:	"application/json;charset=utf-8",
		cache:	false,
		success:	function(returnData){
			returnCallBack(returnData);
		},
		complete:	function(xhr, status){
		},
		error:	function(xhr, status, errorThrow){
		}
	});
}


/**
 * Post 방식으로 페이지를 이동한다. 
 * uri : 이동할 페이지
 */

function goMainPage(uri) {
	var form = document.createElement('form');
	form.setAttribute('method', 'post');
	form.setAttribute('action', uri);
	document.body.appendChild(form);
	form.submit();
}
function goPage(uri) {
	var form = document.createElement('form');
	form.setAttribute('method', 'get');
	form.setAttribute('action', uri);
	document.body.appendChild(form);
	form.submit();
}
// 새 창으로 팝업 화면을 띄울때 사용하는 펑션
function openPopup(url, name, width, height){
	var sw = screen.availWidth; // 스크린 넓이
	var sh = screen.availHeight; // 스크린 높이
	var px = (sw - width) / 2; // x좌표
	var py = (sh - height) / 2; // y좌표
	// 화면 중앙에 모달 띄우게 설정
	window.open(url, name, "width= " + width + ", height=" + height + ", toolbar=no, status=no," +
	"menubar=no, resizable=no, left=" + px + ", top=" + py + ", position=fixed");
	
}

function loadModalObj(modalData, data){
	var tagId = "#" + modalData.id;
	$("body").append("<div id='" + modalData.id + "Area' class='modalArea'></div>");
	$("#" + modalData.id + "Area").data("layer", $("body").find(".modalArea").length);
	$(tagId + "Area").load(modalData.url, {objectId:modalData.id}, function(){
		$(tagId).css({
			"width" : modalData.width,
			"height" : modalData.height,
			"min-width" : modalData.width,
			"min-height" : modalData.height,
			"left" : ($(window).width() - modalData.width) / 2,
			"top" : ($(window).height() - modalData.height) / 2,
			"display" : "block",
			"position" : "absolute"
		}).data("level", modalData.level).css("z-index", 200 * modalData.level);
	})
	
	var modalDataTagId = "#" + modalData.id + "DataBox";
	var innerHtml = "<div id='" + modalData.id + "DataBox'>";
	$.each(data, function(key, value){
		innerHtml += "<input type='hidden' name='" + key + "'value='" + value + "'/>";
	})
	innerHtml += "</div>";
	
	$("body").append(innerHtml);
}



// 드롭다운 공통 구성 함수
function setSelbox(objectId, url, param) {
	var tagId = "#" + objectId;
	ajax(url, param, function(returnData){
		var codeList = returnData.codeList;
		for(var i = 0; i < codeList.length; i++) {
			$(tagId).append("<li class = 'dropdown-item' value='" + codeList[i].comCdNm + "'>" + codeList[i].comCdNm + "</li>")
		}
	})
}

function nullChk(object){
	if(!object) {
		return null;
	} else {
		return object;
	}
}
