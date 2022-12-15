window.onload = function(){
    //ローカルストレージの初期化
    let reset = window.localStorage.getItem("reset");
    console.log(reset)
    if (reset == null){
        localStorage.setItem("reset", 1);
        let x = 1;
        var xhr = new XMLHttpRequest();
        xhr.open("POST", '/reset', true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.send("reset="+x);
    }
}

function change_recommend(e){
    if(e.textContent == "推薦あり"){
        e.textContent = "推薦なし"
        localStorage.setItem("recommend_style", 0);
    }else{
        e.textContent = "推薦あり"
        localStorage.setItem("recommend_style", 1);
    }
    let x = Number(window.localStorage.getItem("recommend_style"));
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/style', true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("style="+x);
}