$(document).ready(function () {
	// 変数に要素を入れる
	var open = $('.articles__add-btn'),
		close = $('.modal-close'),
		container = $('.modal-container');

	//開くボタンをクリックしたらモーダルを表示する
	open.on('click',function(){	
		container.addClass('active');
		return false;
	});

	//閉じるボタンをクリックしたらモーダルを閉じる
	close.on('click',function(){	
		container.removeClass('active');
	});

	//モーダルの外側をクリックしたらモーダルを閉じる
	$(document).on('click',function(e) {
		if(!$(e.target).closest('.modal-body').length) {
			container.removeClass('active');
		}
	});

	let today = new Date();
    today.setDate(today.getDate());
    const YYYY = today.getFullYear();
    const MM = ("0"+(today.getMonth()+1)).slice(-2);
    const DD = ("0"+today.getDate()).slice(-2);
    document.getElementById("id_published_at").value=YYYY+'-'+MM+'-'+DD;
    document.getElementById("id_updated_at").value=YYYY+'-'+MM+'-'+DD;


});