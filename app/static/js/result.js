

window.document.onkeydown = function(event){
	if (event.key === 'Enter') {
		//指定した範囲のテキストの文字を変更
		var selObj = window.getSelection();
		if (selObj == '') {return false;}
		var range = selObj.getRangeAt(0);
		var span = document.createElement("span");
		span.style.color = "#ff0000";
		range.surroundContents(span);

		//チャットボックスに表示
		var message = document.getElementById("attention_word");
		message.innerHTML = ">>>" + range.toString();
	}
}

$(function () {
	$('.js-close').click(function () {
	  window.location.href = "/result";
	});
  });

