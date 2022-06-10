
// window.onload = function() {
// 	const spinner = document.getElementById('loading');
// 	spinner.classList.add('loaded');
// }


window.document.onkeydown = function(event){
	if (event.key === 'Enter') {
		//指定した範囲のテキストの文字を変更
		var selObj = window.getSelection();
		if (selObj == '') {return false;}
		var range = selObj.getRangeAt(0);
		var span = document.createElement("span");
		span.style.color = "#ff0000";
		range.surroundContents(span);
		var id = "#" + range.startContainer.id;

		//チャットボックスに表示
		// var message = document.getElementById("attention_word");
		var message = document.getElementById("reason");
		var text = "＞＞＞" + range.toString();
		message.innerHTML = text;

		// var xhr = new XMLHttpRequest();
		// xhr.open("POST", '/server', true);
		// xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
		// xhr.send("name="+text);

		document.getElementById("submit").click();

	}
}

$(function () {
	$('.js-close').click(function () {
	  window.location.href = "/result";
	});
  });

