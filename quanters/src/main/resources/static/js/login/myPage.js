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
        $('#gridTable').append("<tr><td class='gridTd'><input class='chkBox' type=\"checkbox\" value=" + stockCodeArr[element] + ">" + stockCodeArr[element] +"</td></tr>>")
    }
    showMyStockInfo();

    $('#gridBtn').click(function () {
        var reply = confirm("등록 하시겠습니까?");
        if(reply) {
            const chkArr = $('.chkBox:checked')
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

    function showMyStockInfo() {
        postajax("/stock/showUserStock", {}, function (returnData) {
            var myStockInfo = returnData.stockList;
            $('#myGridTable').empty()
            myStockInfo.forEach(function (value) {
                $('#myGridTable').append("<tr><td class='gridTd'><input class='chkBox' type=\"checkbox\" value=" + value.stockName + ">" + value.stockName +"</td></tr>>")
            })
        })
    }
});