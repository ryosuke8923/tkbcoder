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
	console.log(hiright);
	console.log(JSON.parse(x));
}

// console.log(node);
// console.log(edge);

window.onload = function() {
	
	for(let i = 0; i < hiright.length; i++){
		console.log(hiright[i])
		const a = hiright[i].id
		const b = hiright[i].startOffset;
		const c = hiright[i].endOffset;
		const d = hiright[i].text;


		// idでノードを取得
		let foo = document.getElementById(Number(a));
		console.log(foo);
		let reg = new RegExp(d);
		console.log(1);
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

let tmp_range = "";
let tmp_node = "";
//テキスト範囲選択
window.document.onkeydown = function(event){
	if (event.key === 'Enter') {
		//指定した範囲のテキストの文字を変更
		var selObj = window.getSelection();
		if (selObj == '') {return false;}
		var range = selObj.getRangeAt(0);
		var span = document.createElement("span");
		span.style.color = "#ff0000";
		range.surroundContents(span);
		// var id = "#" + range.startContainer.id;

		//idでノードを取得
		// const foo = document.getElementById(a);
		//新たにRangeオブジェクトを作成→スタート・エンドを決定.
		// var ra = new Range();
		// ra.setStart(foo,b);
		// ra.setEnd(foo,c);

		//テキスト化
		// const text = range.toString();
		// console.log(text); 

		//チャットボックスに表示
		// var message = document.getElementById("attention_word");
		
		// var message = document.getElementById("reason");
		// var text = "＞＞＞" + range.toString();
		// message.innerHTML = text;
		// document.getElementById("submit").click();


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

		

	}
}

//メモ送信した時
function get_message(j=""){
	const textbox = document.getElementById("reason");
	let memo = textbox.value;
	if (j==""){
		let show_memo = tmp_range + "　"+ memo;
		const x = "<div class='user_comment'><div class='user right'><div class='suggest_content' id='suggest_content'><p>"+show_memo+"</p></div></div></div>";
	
		let y = document.getElementById("suggest");
		y.insertAdjacentHTML("beforeend",x);
	}
	// /memo にデータを送信 
	let pattern = /^\$TAG\$/g; 
	if(memo.match(pattern)){
		console.log(12);
		var xhr = new XMLHttpRequest();
		xhr.open("POST", '/node_tag', true);
		xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
		if(j== ""){
			xhr.send("node="+tmp_range+"&tag="+memo);
		}else{
			xhr.send("node="+j+"&tag="+memo);
		}	
		document.getElementById("reason").value = "";
	
	}else{
		var xhr = new XMLHttpRequest();
		xhr.open("POST", '/memo', true);
		xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
		xhr.send("memo="+memo+"&tmp_range="+tmp_range);
		document.getElementById("reason").value = "";
		console.log(10);
	}
	// var xhr = new XMLHttpRequest();
	// xhr.open("POST", '/memo', true);
	// xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	// xhr.send("memo="+memo+"&tmp_range="+tmp_range);

	// document.getElementById("reason").value = "";

}

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


$(function(){
    $('.js-modal-open').on('click',function(){
        $('.js-modal').fadeIn();
        return false;
    });
    $('.js-modal-close').on('click',function(){
        $('.js-modal').fadeOut();
        return false;
    });
	$(".ok").on("click",function(){
		alert("ok");
	});
	$(".no").on("click",function(){
		alert("No");
	});
});