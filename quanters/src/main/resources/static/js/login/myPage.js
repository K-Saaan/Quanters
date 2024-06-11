document.addEventListener('DOMContentLoaded', function () {
    var stockCode = $('#hiddenStockList').text();
    $('#hiddenStockList').hide()
    stockCode = stockCode.replaceAll('[','')
    stockCode = stockCode.replaceAll(']','')
    stockCodeArr = stockCode.split(',');
    $.each(stockCodeArr, function (index, value) {
        stockCodeArr[index] = value.trim()
    })

    // 첫번째 그리드를 그리기 위한 사전 설정
    const container = document.getElementById('stockGrid');
    const provider = new RealGrid.LocalDataProvider(false);
    const gridView = new RealGrid.GridView(container);
    // 두번째 그리드를 그리기 위한 사전 설정
    const subcontainer = document.getElementById('stockGrid2');
    const subprovider = new RealGrid.LocalDataProvider(false);
    const subgridView = new RealGrid.GridView(subcontainer);
    // 세번째 그리드를 그리기 위한 사전 설정
    const thirdcontainer = document.getElementById('stockGrid3');
    const thirdprovider = new RealGrid.LocalDataProvider(false);
    const thirdgridView = new RealGrid.GridView(thirdcontainer);

    gridView.setDataSource(provider);
    gridView.setEditOptions({editable : false}); // 더블클릭시 그리드 셀 수정 불가능하게 설정
    gridView.displayOptions.fitStyle = "fill";
    subgridView.setDataSource(subprovider);
    subgridView.setEditOptions({editable : false}); // 더블클릭시 그리드 셀 수정 불가능하게 설정
    subgridView.displayOptions.fitStyle = "fill";
    thirdgridView.setDataSource(thirdprovider);
    thirdgridView.setEditOptions({editable : false}); // 더블클릭시 그리드 셀 수정 불가능하게 설정
    thirdgridView.displayOptions.fitStyle = "fill";

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
            fieldName: "stockCode",
            dataType: "text",
        },
        {
            fieldName: "stockName",
            dataType: "text",
        },
    ]);

    subgridView.setColumns([
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
    thirdprovider.setFields([
        {
            fieldName: "stockCode",
            dataType: "text",
        },
        {
            fieldName: "stockName",
            dataType: "text",
        },
        {
            fieldName: "stockDate",
            dataType: "text",
        },
        {
            fieldName: "openPrice",
            dataType: "text",
        },
        {
            fieldName: "highPrice",
            dataType: "text",
        },
        {
            fieldName: "lowPrice",
            dataType: "text",
        },
        {
            fieldName: "closePrice",
            dataType: "text",
        },
        {
            fieldName: "stockVolume",
            dataType: "text",
        },
        {
            fieldName: "stockChange",
            dataType: "text",
        },
    ]);

    thirdgridView.setColumns([
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
        {
            name: "stockDate",
            fieldName: "stockDate",
            type: "data",
            width: "120",
            header: {
                text: "날짜",
            },
        },
        {
            name: "openPrice",
            fieldName: "openPrice",
            type: "data",
            width: "120",
            header: {
                text: "시가",
            },
        },
        {
            name: "highPrice",
            fieldName: "highPrice",
            type: "data",
            width: "120",
            header: {
                text: "고가",
            },
        },
        {
            name: "lowPrice",
            fieldName: "lowPrice",
            type: "data",
            width: "120",
            header: {
                text: "저가",
            },
        },
        {
            name: "closePrice",
            fieldName: "closePrice",
            type: "data",
            width: "120",
            header: {
                text: "종가",
            },
        },
        {
            name: "stockVolume",
            fieldName: "stockVolume",
            type: "data",
            width: "120",
            header: {
                text: "거래량",
            },
        },
        {
            name: "stockChange",
            fieldName: "stockChange",
            type: "data",
            width: "120",
            header: {
                text: "변화율",
            },
        },
    ]);

    postajax("/stock/showAllStock", {}, function(returnData){
        var detailData = returnData.stockList;
        provider.fillJsonData(detailData, { fillMode : "set"});
    })

    // 두번째 그리드 그리는 동작
    showMyStockInfo();

    // 일단 예측 이미지는 가려두고
    $("#upImage").hide()
    $("#downImage").hide()

    // 추가 동작
    $('#gridBtn').click(function () {
        var chkArr = gridView.getCheckedRows();
        var reply = confirm("등록 하시겠습니까?");
        if(reply) {
            var resultArr = []
            for(var i in chkArr) {
                var chkStock = provider.getJsonRow(chkArr[i]);
                resultArr.push(chkStock.stockCode)
            }
            var param = {
                stockCode: resultArr
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

    // 두번째 그리드 채워넣는 동작
    function showMyStockInfo() {
        postajax("/stock/showUserStock", {}, function (returnData) {
            var myStockInfo = returnData.stockList;
            subprovider.fillJsonData(myStockInfo, { fillMode : "set"});
            gridDblCellClicked();
        })
    }

    function showStockHist(stockCode) {
        var histParam = {
            "stockCode" : stockCode
        }
        postajax("/stock/showStockHist", histParam, function(returnData){
            var detailData = returnData.stockList;
            thirdprovider.fillJsonData(detailData, { fillMode : "set"});
        })
    }

    function showStockPredict(stockName) {
        var predictParam = {
            "stockName" : stockName
        }
        postajax("/stock/showStockPredict", predictParam, function(returnData){
            var resultMsg = returnData.resultMsg;
            if(resultMsg == "up") {
                $("#upImage").show()
                $("#downImage").hide()
            } else {
                $("#downImage").show()
                $("#upImage").hide()
            }
        })
    }

    // 두번째 그리드 더블클릭했을때 모달 호출
    function gridDblCellClicked(){
        subgridView.onCellDblClicked = function(grid, clickData){
            var selectOneData = subgridView.getDataSource().getJsonRow(subgridView.getCurrent().dataRow);
            var stockCode = selectOneData.stockCode;
            var stockName = selectOneData.stockName;
            showStockHist(stockCode)
            showStockPredict(stockName)
        }
    }

});