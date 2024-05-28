document.addEventListener('DOMContentLoaded', function () {
    var stockCode = $('#hiddenStockList').text();
    $('#hiddenStockList').hide()
    stockCode = stockCode.replaceAll('[','')
    stockCode = stockCode.replaceAll(']','')
    stockCodeArr = stockCode.split(',');
    $.each(stockCodeArr, function (index, value) {
        stockCodeArr[index] = value.trim()
    })

    for(const element in stockCodeArr) {
        $('#gridTable').append("<tr><td class='gridTd'><input class='chkBox leftChk' type=\"checkbox\" value=" + stockCodeArr[element] + ">" + stockCodeArr[element] +"</td></tr>>")
    }
    showMyStockInfo();

    // 추가 동작
    $('#gridBtn').click(function () {
        var reply = confirm("등록 하시겠습니까?");
        if(reply) {
            const chkArr = $('.leftChk:checked')
            var resultArr = []
            chkArr.each(function () {
                resultArr.push($(this).val())
            })
            var param = {
                stockName: resultArr
            };
            postajax("/stock/insertUserStock", param, function (returnData) {
                if (returnData == 1) {
                    alert("등록이 완료됐습니다.");
                    showMyStockInfo();
                } else {
                    alert("등록 실패..");
                }
            })
        }
    })

    // 삭제 동작
    $('#gridBtn2').click(function () {
        var reply = confirm("삭제 하시겠습니까?");
        if(reply) {
            const chkArr = $('.rightChk:checked')
            var resultArr = []
            chkArr.each(function () {
                resultArr.push($(this).val())
            })
            var param = {
                stockName: resultArr
            };
            postajax("/stock/deleteUserStock", param, function (returnData) {
                if (returnData == 1) {
                    alert("삭제가 완료됐습니다.");
                    showMyStockInfo();
                } else {
                    alert("삭제 실패..");
                }
            })
        }
    });

    function showMyStockInfo() {
        postajax("/stock/showUserStock", {}, function (returnData) {
            var myStockInfo = returnData.stockList;
            $('#myGridTable').empty()
            myStockInfo.forEach(function (value) {
                $('#myGridTable').append("<tr><td class='gridTd'><input class='chkBox rightChk' type=\"checkbox\" value=" + value.stockName + ">" + value.stockName +"</td></tr>>")
            })
        })
        $('.chkBox:checked').prop("checked", false)
    }
});