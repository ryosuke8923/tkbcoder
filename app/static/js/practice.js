
//==================関数群==========================


//=============フロントにタグを表示させる関数============
function show_tag(hiright_id,content){

	var css = `
	.${hiright_id}{
		background-color: lightgreen;
		border-radius: 100vh;
		font-weight: bolder;
		font-size: 1em;
	}
	.${hiright_id}::before{content:'  ${content}   ';color:red;}
	`;
	// 
	var style = $('<style>');
	style.text(css);
	$('body').append(style);
}
//=============フロントにタグを表示させる関数============


//==========分析者がタグを送信してきた場合=================
function input_tag(){
	//分析者の入力内容を受け取る
	let input_tag = document.getElementById("input_tag_text").value;
	//非同期通信によるデータの送信

	//フォームの入力値を初期化しておく
	document.getElementById("input_tag_text").value = '';
	//フォームを消す
	$('.js-modal').fadeOut();

	let unique_id = window.localStorage.getItem("id");
	hiright_id = "hiright_" + unique_id;
	show_tag(hiright_id,input_tag);
	localStorage.setItem("id", Number(unique_id)+1);
}
//==========分析者がタグを送信してきた場合=================

//===================タグの削除========================
// function remove_tag(){
// 	//フロント上での削除
// 	let unique_id = window.localStorage.getItem("id");
// 	let target_id = Number(unique_id)-1;
// 	let target = document.getElementsByClassName(target_id)[0];
// 	target.parentNode.removeChild(target);

// 	let input_tag = "system_delete_tag"
// 	var xhr = new XMLHttpRequest();
// 	xhr.open("POST", '/input_tag', true);
// 	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
// 	xhr.send("input_tag="+input_tag);
// }
//===================タグの削除========================



// =====推薦候補に対して分析者のアクションがあった場合========
function apply_recommend(e){

	
	if(e.className == "apply"){
        //rangeにハイライトを塗るためにspanタグを準備
		var span = document.getElementsByClassName("target")[0];
		span.setAttribute('ondblclick', 'remove_tag(this)');
		span.style.color = "black";

	    show_tag("target","テスト");
       
        document.getElementsByClassName("suggest_data")[0].remove();
	}

}
// =====推薦候補に対して分析者のアクションがあった場合========


function remove_tag(e){
   location.reload();
}

// ==================関数群============================

function hello(e){
	console.log("1")
	console.log(e)
	let regexp_id = /(?<=recommend_id_).+/;
	// id取得
	let id = regexp_id.exec(e.id)[0];
	let string1 = "recommend_sentence_"+id;
	let sentence1 = document.getElementById(string1).textContent;
	sentence1 = sentence1.replace(/^\s/,"")
	let change = "<div style='color:#ff0000'>"+sentence1+"</div>"
	let tmp_node = document.getElementById(Number(id)+1);
	reg = new RegExp(sentence1);
	tmp_node.innerHTML = tmp_node.innerHTML.replace(reg,change)
}
function all_tag(e){
	let tag_modal = document.getElementById("tag_modal");
	tag_modal.style.display = "block";
	
}
function hidden_all_tag(e){
	let tag_modal = document.getElementById("tag_modal");
	tag_modal.style.display = "none";
}


function check_rec_level(e){

	if(e.textContent == "推薦頻度：低"){
		e.textContent = "推薦頻度：普"
	}else if (e.textContent == "推薦頻度：普"){
		e.textContent = "推薦頻度：高"
	}else{
		e.textContent = "推薦頻度：低"
	}
}
// =================変数の初期化========================
let tmp_range = "";
let tmp_node = "";

// =================変数の初期化========================


// Loading Action
// ================タグ付与部分の再現====================
window.onload = function() {

	
	
	

		
}
// ================タグ付与部分の再現====================

// ===================キーイベント======================
window.document.onkeydown = function(event){
	// shift+enterでタグ送信
	if (event.shiftKey && event.keyCode === 88){
		location.reload();
	}
	if (event.shiftKey && event.keyCode === 90 && document.getElementById("input_tag_text").value != "") {
		if(document.getElementById("input_tag_text").value != "");{
			document.getElementById("input_tag_button").click();
		}
		return false;
	}
	// 範囲選択＋enterでタグを付与する文章の選択&タグ入力フォーム出現
	if (event.shiftKey && event.key === 'Enter') {
        let unique_id = window.localStorage.getItem("id");
		if (unique_id === null){
			unique_id = 0;
			localStorage.setItem("id", 0);
		}
		
		//range 指定した範囲を取得
		var selObj = window.getSelection();
		if (selObj == '') {return false;}
		var range = selObj.getRangeAt(0);

		//rangeにハイライトを塗るためにspanタグを準備
		var span = document.createElement("button");
		span.setAttribute('ondblclick', 'remove_tag(this)');
		span.style.color = "black";

		//cssを適用するためにspanタグにclassを追加 
		hiright_id = "hiright_" + unique_id;
		span.setAttribute("class",hiright_id);

		//指定した範囲にspanタグを挿入
		range.surroundContents(span);

		var css = `
		.${hiright_id}{
			background-color: lightgreen;
			border-radius: 100vh;
			font-weight: bolder;
			font-size: 1em;
		}`;
		// 
		var style = $('<style>');
		style.text(css);
		$('body').append(style);

		//タグ入力フォーム出現
		$('.js-modal').fadeIn();
		let input_tag = document.getElementById("input_tag_text");
		input_tag.focus();
		
	}
}
// ===================キーイベント======================

