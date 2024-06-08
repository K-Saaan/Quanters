document.addEventListener('DOMContentLoaded', function () {
    var stockCode = $('#hiddenStockList').text();
    $('#hiddenStockList').hide()
    stockCode = stockCode.replaceAll('[','')
    stockCode = stockCode.replaceAll(']','')
    stockCodeArr = stockCode.split(',');
    $.each(stockCodeArr, function (index, value) {
        stockCodeArr[index] = value.trim()
    })

    // 메인그리드를 그리기 위한 사전 설정
    const container = document.getElementById('stockGrid');
    const provider = new RealGrid.LocalDataProvider(false);
    const gridView = new RealGrid.GridView(container);
    // 서브그리드를 그리기 위한 사전 설정
    const subcontainer = document.getElementById('stockGrid2');
    const subprovider = new RealGrid.LocalDataProvider(false);
    const subgridView = new RealGrid.GridView(subcontainer);

    gridView.setDataSource(provider);
    gridView.setEditOptions({editable : false}); // 더블클릭시 그리드 셀 수정 불가능하게 설정
    gridView.displayOptions.fitStyle = "fill";
    subgridView.setDataSource(subprovider);
    subgridView.setEditOptions({editable : false}); // 더블클릭시 그리드 셀 수정 불가능하게 설정
    subgridView.displayOptions.fitStyle = "fill";

    // 메인그리드 컬럼
    provider.setFields([
        {
            fieldName: "stockCode",
            dataType: "text",
        },
        {
            fieldName: "stockName",
            dataType: "text",
        },
    ]);

    gridView.setColumns([
        {
            name: "stockCode",
            fieldName: "stockCode",
            type: "data",
            width: "120",
            header: {
                text: "주가코드",
            },
        },
        {
            name: "stockName",
            fieldName: "stockName",
            type: "data",
            width: "120",
            header: {
                text: "주가명",
            },
        },
    ]);

    // 서브그리드 컬럼
    subprovider.setFields([
        {
            fieldName: "stockName",
            dataType: "text",
        },
    ]);

    subgridView.setColumns([
        {
            name: "stockName",
            fieldName: "stockName",
            type: "data",
            width: "120",
            header: {
                text: "주가명",
            },
        },
    ]);

    postajax("/stock/showAllStock", {}, function(returnData){
        var detailData = returnData.stockList;
        provider.fillJsonData(detailData, { fillMode : "set"});
    })

    showMyStockInfo();

    // 추가 동작
    $('#gridBtn').click(function () {
        var chkArr = gridView.getCheckedRows();
        var reply = confirm("등록 하시겠습니까?");
        if(reply) {
            var resultArr = []
            for(var i in chkArr) {
                var chkStock = provider.getJsonRow(chkArr[i]);
                resultArr.push(chkStock.stockName)
            }
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
        var chkArr = subgridView.getCheckedRows();
        var reply = confirm("삭제 하시겠습니까?");
        if(reply) {
            var resultArr = []
            for(var i in chkArr) {
                var chkStock = subprovider.getJsonRow(chkArr[i]);
                resultArr.push(chkStock.stockName)
            }
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
            subprovider.fillJsonData(myStockInfo, { fillMode : "set"});
        })
    }

});