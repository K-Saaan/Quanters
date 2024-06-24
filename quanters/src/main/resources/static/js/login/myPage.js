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
            width: "90",
            header: {
                text: "주가코드",
            },
        },
        {
            name: "stockName",
            fieldName: "stockName",
            type: "data",
            width: "90",
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
            width: "90",
            header: {
                text: "주가코드",
            },
        },
        {
            name: "stockName",
            fieldName: "stockName",
            type: "data",
            width: "90",
            header: {
                text: "주가명",
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
            // thirdprovider.fillJsonData(detailData, { fillMode : "set"});
            var stockDateArr = []
            var openPriceArr = []
            var highPriceArr = []
            var lowPriceArr = []
            var closePriceArr = []
            detailData.forEach(function (value) {
                stockDateArr.push(value.stockDate)
                openPriceArr.push(value.openPrice)
                highPriceArr.push(value.highPrice)
                lowPriceArr.push(value.lowPrice)
                closePriceArr.push(value.closePrice)
            })
            var todayData = closePriceArr[0]
            var yesterdayData = closePriceArr[1]
            var minusData = todayData - yesterdayData
            $("#priceDiff").text(minusData)
            // 어제 대비 올랐으면 빨간색 내려갔으면 파란색으로 증감 텍스트 표시
            if(minusData > 0) {
                $("#priceDiff").css('color','red')
            } else {
                $("#priceDiff").css('color','blue')
            }
            // 차트 그래프 그리기
            drawStockGraph(stockDateArr.reverse(), openPriceArr.reverse(), highPriceArr.reverse(), lowPriceArr.reverse(), closePriceArr.reverse());
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
            } else if(resultMsg == "down") {
                $("#downImage").show()
                $("#upImage").hide()
            } else if(resultMsg == "error") {
                $("#downImage").hide()
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

    // 최근 일주일 데이터만 보이게 설정
    var oneWeekMs = 7 * 24 * 60 * 60 * 1000; // 일주일의 밀리초
    var now = new Date().getTime();
    var oneWeekAgo = now - oneWeekMs;

    function drawStockGraph(stockDateArr, openPriceArr, highPriceArr, lowPriceArr, closePriceArr) {
        var chart = echarts.init(document.getElementById('stockGraph'));
        var option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross'
                },
                formatter: function (params) {
                    let result = params[0].name + '<br>';
                    for (let i = 0; i < params.length; i++) {
                        var textColor = params[i].color;
                        result += '<p style="color: ' + textColor + ' "' + '>' + params[i].seriesName + ': ' + params[i].value + '</p>';
                    }
                    return result;
                }
            },
            dataZoom: [
                {
                    type: 'slider',
                    show: true,
                    start: 90,
                    end: 100
                }
            ],
            legend: {
            },
            xAxis: {
                type: 'category',
                data: stockDateArr
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name: '시가',
                    type: 'line',
                    data: openPriceArr
                },
                {
                    name: '고가',
                    type: 'line',
                    data: highPriceArr
                },
                {
                    name: '저가',
                    type: 'line',
                    data: lowPriceArr
                },
                {
                    name: '종가',
                    type: 'line',
                    data: closePriceArr
                }
            ]
        };
        chart.setOption(option);
    }
});