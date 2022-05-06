

$(function () {
   
    $('#overlay, .modal-window').hide();
    
	$('.js-open').click(function () {
	  $('#overlay, .modal-window').fadeIn();
	});

	$('.js-close').click(function () {
	//   var $checkbutton = $("#sentence");
	//   console.log($checkbutton);
	//   console.log($checkbutton[0].val());
	//   console.log($checkbutton[3]);
	  $('#overlay, .modal-window').fadeOut();
	  window.location.href = "/result";
	});
  });

