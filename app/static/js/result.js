// let hiright = $('#hiright').data("name");
// const node = $('#node').data();
// const edge = $('#edge').data();
// for(let i = 0; i < hiright.length; i++){
// 	console.log(hiright[i]);
// }
console.log(hiright);
console.log(typeof(hiright));
if (hiright==[]){
	let x = hiright.slice(1,-1);
	x = x.replace(/\'/g, "\"");
	console.log(x);
	hiright = JSON.parse(x);
	console.log(1,hiright);
	console.log(JSON.parse(x));
}

// console.log(node);
// console.log(edge);

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
	
}
//==========分析者がタグを送信してきた場合=================

// =====推薦候補に対して分析者のアクションがあった場合========
function apply_recommend(e){
	// 押したボタンの推薦文章とタグを抽出するためのパターン
	let regexp1 = /(?<=文章：).+/;
	let regexp2 = /(?<=タグ：).+/;
	let regexp_id = /(?<=apply_).+/;
	// id取得
	let id = regexp_id.exec(e.id)[0];
	if(e.className == "apply"){
		// 1→文章に関するもの 2→タグに関するもの
		let string1 = "recommend_sentence_"+id;
		let string2 = "recommend_tag_"+id
		let sentence1 = document.getElementById(string1).textContent;
		let sentence2 = document.getElementById(string2).textContent;
		let result1 = regexp1.exec(sentence1);
		let result2 = regexp2.exec(sentence2);
		// タグ付与操作
		console.log(result1[0],result2[0]);
		console.log("操作します");
	}
	// フロント上の削除
	let string = "#suggest_data_"+id
	console.log(string);
	$(string).remove();

	//flaskでの削除
}
// =====推薦候補に対して分析者のアクションがあった場合========


window.addEventListener("load", function(){
	// ストレージチェック
	let x = localStorage.getItem("x")
	let y = localStorage.getItem("y")
	console.log(x,y);
	// 前回の保存データがあればスクロールする
	if(y !== null){
		console.log(8888)
	}

	// スクロール時のイベント設定
});
// ================タグ付与部分の再現====================
window.onload = function() {

	for(let i = 0; i < hiright.length; i++){
		console.log(hiright[i])
		const a = hiright[i].id
		const b = hiright[i].startOffset;
		const c = hiright[i].endOffset;
		const d = hiright[i].text;

		console.log(a)
		// idでノードを取得
		let foo = document.getElementById(Number(a));
		console.log(1,foo);
		let reg = new RegExp(d);
		console.log(1);
		// let start_index = foo.firstChild.data.match(reg).index;
		console.log(reg)
		let start_index = foo.firstChild.data.match(reg).index;
		console.log(foo);
		console.log(2);
		let end_index = start_index + d.length;

		// 新たにRangeオブジェクトを作成→スタート・エンドを決定.
		var ra = new Range();
		ra.setStart(foo.firstChild,start_index);
		ra.setEnd(foo.firstChild,end_index);

		var span = document.createElement("span");
		span.style.color = "#ff0000";
		ra.surroundContents(span);
	}
}
// ================タグ付与部分の再現====================


let tmp_range = "";
let tmp_node = "";
//テキスト範囲選択


// ===================キーイベント======================
window.document.onkeydown = function(event){
	// shift+enterでタグ送信
	if (event.shiftKey && event.key === 'Enter') {
		if(document.getElementById("input_tag_text").value != "");{
			document.getElementById("input_tag_button").click();
		}
		return false;
	}
	// 範囲選択＋enterでタグを付与する文章の選択&タグ入力フォーム出現
	if (event.key === 'Enter') {
        
		//指定した範囲のテキストの文字を変更
		var selObj = window.getSelection();
		if (selObj == '') {return false;}
	
		var range = selObj.getRangeAt(0);
		var span = document.createElement("span");
		
		span.style.color = "#ff0000";
		range.surroundContents(span);

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
		//タグ入力フォーム出現
		$('.js-modal').fadeIn();
		var targetElement = document.getElementById( a ) ;
		var clientRect = targetElement.getBoundingClientRect() ;
		var x = clientRect.left ;
		var y = clientRect.top ;
		localStorage.setItem("x", x);
		localStorage.setItem("y", y);
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