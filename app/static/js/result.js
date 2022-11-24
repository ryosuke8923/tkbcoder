// let hiright = $('#hiright').data("name");
// const node = $('#node').data();
// const edge = $('#edge').data();
// for(let i = 0; i < hiright.length; i++){
// 	console.log(hiright[i]);
// }
// console.log(hiright);
// console.log(typeof(hiright));
// if (hiright==[]){
// 	let x = hiright.slice(1,-1);
// 	x = x.replace(/\'/g, "\"");
// 	console.log(x);
// 	hiright = JSON.parse(x);
// 	console.log(1,hiright);
// 	console.log(JSON.parse(x));
// }

// console.log(node);
// console.log(edge);


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
	var xhr = new XMLHttpRequest();
	xhr.open("POST", '/input_tag', true);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	xhr.send("input_tag="+input_tag);
	//フォームの入力値を初期化しておく
	document.getElementById("input_tag_text").value = '';
	//フォームを消す
	$('.js-modal').fadeOut();
	location.reload();

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
	// 押したボタンの推薦文章とタグを抽出するためのパターン
	let regexp_id = /(?<=apply_).+/;
	// id取得
	let id = regexp_id.exec(e.id)[0];
	
	if(e.className == "apply"){
		// 1→文章に関するもの 2→タグに関するもの
		let string1 = "recommend_sentence_"+id;
		let string2 = "recommend_tag_"+id
		let sentence1 = document.getElementById(string1).textContent;
		let sentence2 = document.getElementById(string2).textContent;
		console.log("適用する");
		console.log(sentence1,sentence2);
		id = String(Number(id)+1);
		console.log(id);
		const a= id;
		const b = 0;
		const c= 0;
		const d = sentence1.trim();
		const e = sentence2.trim();

		var xhr = new XMLHttpRequest();
		xhr.open("POST", '/hiright', true);
		xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
		console.log(a,b,c,d)
		xhr.send("a="+a+"&b="+b+"&c="+c+"&d="+d);

		console.log(8888)
		var xhr = new XMLHttpRequest();
		xhr.open("POST", '/input_tag', true);
		xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
		xhr.send("input_tag="+e);

		let unique_id = window.localStorage.getItem("id");
		localStorage.setItem("id", Number(unique_id)+1);
		localStorage.setItem("page_anchor", a);
		// location.reload();
		id = String(Number(id)-1);
	}

	let string1 = "recommend_sentence_"+id;
	let sentence1 = document.getElementById(string1).textContent;
	const d = sentence1.trim();

	var xhr = new XMLHttpRequest();
	xhr.open("POST", '/remove_recommend', true);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	xhr.send("remove_recommend="+d);
	
	// フロント上の削除
	// let string = "#suggest_data_"+id
	// console.log(string);
	// $(string).remove();

	//flaskでの削除
	location.reload();
}
// =====推薦候補に対して分析者のアクションがあった場合========


function remove_tag(e){
	let text = e.innerText;
	console.log(text);
	var xhr = new XMLHttpRequest();
	xhr.open("POST", '/remove_tag', true);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	xhr.send("remove_tag="+text);
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

function show_howtouse(e){
	let tag_modal = document.getElementById("howtouse_modal");
	tag_modal.style.display = "block";
	
}
function hidden_howtouse(e){
	let tag_modal = document.getElementById("howtouse_modal");
	tag_modal.style.display = "none";
}

function check_rec_level(e){
	var xhr = new XMLHttpRequest();
	xhr.open("POST", '/rec_level', true);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	if(e.textContent == "推薦頻度：低"){
		e.textContent = "推薦頻度：普"
		xhr.send("rec_level="+"1");
		localStorage.setItem("rec_level", 1);
	}else if (e.textContent == "推薦頻度：普"){
		e.textContent = "推薦頻度：高"
		xhr.send("rec_level="+"2");
		localStorage.setItem("rec_level", 2);
	}else{
		e.textContent = "推薦頻度：低"
		xhr.send("rec_level="+"0");
		localStorage.setItem("rec_level", 0);
	}
}

function page_top(e){
	let page_anchor = Number(window.localStorage.getItem("page_anchor"));
	if (page_anchor != null){
		localStorage.removeItem("page_anchor");
	}
	location.reload();
}
// =================変数の初期化========================
let tmp_range = "";
let tmp_node = "";

// =================変数の初期化========================


// Loading Action
// ================タグ付与部分の再現====================
window.onload = function() {
	// let input_text = document.getElementById("input_tag_text");
	// input_text.setSuggestions(["ありがとう"])
	console.log(js_tags)
	let keys = Object.keys(js_tags);
	let browsers = document.getElementById("browsers");
	for(let i=0;i<keys.length;i++){
		var new_element = document.createElement('option');
		new_element.value = keys[i];
		browsers.appendChild(new_element);

	}
	let page_anchor = Number(window.localStorage.getItem("page_anchor"));
	let rec_level = Number(window.localStorage.getItem("rec_level"));
	window.location.hash = "";
	if (page_anchor > 2){
		window.location.hash = page_anchor-2;
	}
	let rec_level_btn = document.getElementById("rec_level");
	if (rec_level == 0){
		rec_level_btn.textContent = "推薦頻度：低";
	}else if(rec_level == 1){
		rec_level_btn.textContent = "推薦頻度：普";
	}else{
		rec_level_btn.textContent = "推薦頻度：高";
	}
	
	for(let i = 0; i < hiright.length; i++){
		const a = hiright[i].id
		const b = hiright[i].startOffset;
		const c = hiright[i].endOffset;
		const d = hiright[i].text;
		const e = hiright[i].tag;
		console.log(a,b,c,d,e);
		// idでノードを取得
		let foo = document.getElementById(Number(a));
		
		let reg = new RegExp(d);
		// console.log(i,foo);

		var ra = new Range();

		// let id = regexp_id.exec(e.id)[0];
		// let string1 = "recommend_sentence_"+id;
		// let sentence1 = document.getElementById(string1).textContent;
		// sentence1 = sentence1.replace(/^\s/,"")
		hiright_id = "hiright_" + String(i);
		let change = `<button ondblclick='remove_tag(this)' class='${hiright_id}' style='color: black;'>` +d+`</button>`
		let tmp_node = document.getElementById(Number(a));
		console.log(tmp_node)
		reg = new RegExp(d);
		tmp_node.innerHTML = tmp_node.innerHTML.replace(reg,change)
		show_tag(hiright_id,e);


		// try{
		// 	if(foo.childNodes.length == 1){
		// 		let start_index = foo.firstChild.data.match(reg).index;
		// 		let end_index = start_index + d.length;
		// 		// 新たにRangeオブジェクトを作成→スタート・エンドを決定.
		// 		var ra = new Range();
		// 		console.log(i,foo.firstChild.data);
		// 		ra.setStart(foo.firstChild,start_index);
		// 		ra.setEnd(foo.firstChild,end_index);
				
		// 	}else{
				
		// 		let start_index = foo.lastChild.data.match(reg).index;
		// 		let end_index = start_index + d.length;
		// 		ra.setStart(foo.lastChild,start_index);
		// 		ra.setEnd(foo.lastChild,end_index);
		// 	}
		// 	var span = document.createElement("button");
		// 	span.setAttribute('ondblclick', 'remove_tag(this)');
		// 	span.style.color = "black";
		// 	hiright_id = "hiright_" + String(i);
		// 	span.setAttribute("class",hiright_id);
		// 	ra.surroundContents(span);
		// 	console.log(span);
		// 	show_tag(hiright_id,e);
		// }catch(e){
		// 	console.log(e,i)
		// }
		

		
	}
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

		//reload時に再現できるようにハイライトのデータをflaskに送信
		const a = range.startContainer.id;
		const b = range.startOffset;
		const c = range.endOffset;
		const d = range.toString();
		tmp_range = a
		// /hiright にデータを送信 
		var xhr = new XMLHttpRequest();
		xhr.open("POST", '/hiright', true);
		xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
		xhr.send("a="+a+"&b="+b+"&c="+c+"&d="+d);

		localStorage.setItem("page_anchor", a);
		//タグ入力フォーム出現
		$('.js-modal').fadeIn();
		let input_tag = document.getElementById("input_tag_text");
		input_tag.focus();
		
	}
}
// ===================キーイベント======================

// ===================メモ送信した時====================
// function get_message(j=""){
// 	const textbox = document.getElementById("reason");
// 	let memo = textbox.value;
// 	if (j==""){
// 		let show_memo = tmp_range + "　"+ memo;
// 		const x = "<div class='user_comment'><div class='user right'><div class='suggest_content' id='suggest_content'><p>"+show_memo+"</p></div></div></div>";
	
// 		let y = document.getElementById("suggest");
// 		y.insertAdjacentHTML("beforeend",x);
// 	}
	// /memo にデータを送信 
	// let pattern = /^\$TAG\$/g; 
	// if(memo.match(pattern)){
	// 	console.log(12);
	// 	var xhr = new XMLHttpRequest();
	// 	xhr.open("POST", '/node_tag', true);
	// 	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	// 	if(j== ""){
	// 		xhr.send("node="+tmp_range+"&tag="+memo);
	// 	}else{
	// 		xhr.send("node="+j+"&tag="+memo);
	// 	}	
	// 	document.getElementById("reason").value = "";
	
// 	}else{
// 		var xhr = new XMLHttpRequest();
// 		xhr.open("POST", '/memo', true);
// 		xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
// 		xhr.send("memo="+memo+"&tmp_range="+tmp_range);
// 		document.getElementById("reason").value = "";
// 		console.log(10);
// 	}
// }
// ===================メモ送信した時====================

// =========グラフの表示(make_cy内で呼び出される)=========
function show_cy(){
	let div1 = document.getElementById("cy_button");
	if(div1.value == "グラフを閉じる"){
		let div2 = document.getElementById("cy");
		div2.remove();
		div1.value = "グラフを確認する";
		document.getElementById("submit").style.visibility ="visible";
	}else{
		document.getElementById("submit").style.visibility ="hidden";
		div1.insertAdjacentHTML('afterend','<div id="cy"></div>');
		div1.value = "グラフを閉じる";
		make_cy(node,edge);
	}
	
}
// =========グラフの表示(make_cy内で呼び出される)=========


// ===============グラフノードの作成====================
function make_cy(node,edge){
	var cy = cytoscape({
		container: document.getElementById('cy'),
	  
		boxSelectionEnabled: false,
		autounselectify: true,
	  
		layout: {
		  name: 'dagre'
		},
		style: [
		  {
			selector: 'node',
			style: {
			  'content': 'data(id)',  
			  'background-color': '#11479e'
			}
		  },
		  { 
			selector: 'node[label = "0"]', 
        	css: {'background-color': 'red', 'content': 'data(id)'}
      	  },
			{ 
			selector: 'node[label = "1"]', 
        	css: {'background-color': 'blue', 'content': 'data(id)'}
      	  },
			{ 
				selector: 'node[label = "2"]', 
				css: {'background-color': 'green', 'content': 'data(id)'}
				},
		  {
			selector: 'edge',
			style: {
			  'target-arrow-shape': 'triangle',
			  'curve-style': 'bezier',
			  'target-arrow-color': '#9dbaea',
			  'width': 4,
			  'line-color': '#9dbaea',
			}
		  }
		],
	  
		elements: {
		  "nodes":node, 
		  "edges":edge
		},
		
	  });
	  //クリックしたノードの値を取得
	  cy.unbind('click');
	  cy.bind('click', 'node', function(node) {
		tmp_node = node.target.data().id;
		if(document.getElementById("reason").value != ""){
			get_message(tmp_node);
		}
	  });
}
// ===============グラフノードの作成====================