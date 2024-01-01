document.addEventListener('DOMContentLoaded', function () {
    console.log("home.js")
    var realPath = location.href; // http://localhost:8080/member/show 같은 full URL
    var urlIndex = realPath.lastIndexOf("/");
    var usingUrl = realPath.substring(0, urlIndex); // full URL에서 http://localhost:8080/member 까지만 자른 URL
    var searchUrl = usingUrl + '/detail'
    var searchList = ["삼성전자", "SK하이닉스", "카카오", "네이버"]
    $("#searchText").click(function (e){
        if( $("#searchText").val() == "" ) {
            $(".searchUl").empty();
            for(var i = 0; i < searchList.length; i++) {
                $(".searchUl").append("<li class='searchLi'><a href='#' class='link'>" + searchList[i] + "</a></li>");
            }
        }
    });
    $(document).on('click', ".searchLi a", function (){
        var keyword = $(this).text()
        window.location.href = "/home/detail?keyword=" + keyword;
    })
    // 검색창에 커서가 포커스 됐을 경우 리스트를 show 검색창 각지게 하기
    $("#searchText").focus(function (){
        $(".searchUl").show();
        $(".searchBar").css("border-radius", "0px")
    })
    // 검색창에 커서가 포커스를 잃었을 경우 리스트를 hide 검색창 둥글게 하기
    $("#searchText").blur(function (){
        setTimeout(function (){
            $(".searchUl").hide();
            $(".searchBar").css("border-radius", "40px")
        },200);
    })

    $("#searchText").keyup(function (){
        // 우선 매번 리스트 초기화
        $(".searchUl").empty();
        // 검색창에 입력한 검색어
        const searchVal = $("#searchText").val().trim();
        // 검색어가 기존 리스트에 포함되는지 체크하여 포함되면 배열에 담음
        const matchDataList = searchVal ? searchList.filter((label) => label.includes(searchVal)) : [];
        // 하위 리스트
        var li = $(".searchUl").children();
        // 기존에 만들어진 하위 li가 아무것도 없는 경우
        if(li.length == 0) {
            // 검색어도 아무것도 입력하지 않았을때는 전체 리스트 출력
            if(searchVal == "") {
                for(var i = 0; i < searchList.length; i++) {
                    $(".searchUl").append("<li class='searchLi'><a href='#' class='link'>" + searchList[i] + "</a></li>");
                }
            }
            else {
                // 검색어를 입력했고 검색어에 해당하는 목록이 있었을 경우는 해당하는 목록만 출력
                if(matchDataList.length != 0) {
                    for(var i = 0; i < matchDataList.length; i++) {
                        $(".searchUl").append("<li class='searchLi'><a href='#' class='link'>" + matchDataList[i] + "</a></li>");
                    }
                }
            }
        }
        // 기존에 이미 만들어진 li가 있는 경우
        else {
            // 검색어와 일치하는 목록이 있다면 해당하는 목록만 출력
            if(matchDataList.length != 0) {
                for(var i = 0; i < matchDataList.length; i++) {
                    $(".searchUl").append("<li class='searchLi'><a href='#' class='link'>" + matchDataList[i] + "</a></li>");
                }
            }
        }
    });
    $("#searchText").keypress(function (e){
        if(e.keyCode == 13) {
            var keyword = $("#searchText").val();
            window.location.href = "/home/detail?keyword=" + keyword;
        }
    });
    $("#searchBtn").click(function (){
        var keyword = $("#searchText").val();
        window.location.href = "/home/detail?keyword=" + keyword;
    });
});