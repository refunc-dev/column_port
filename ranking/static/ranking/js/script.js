$(document).ready(function () {
	// 変数に要素を入れる
	var open_add = $('.keyword__add-btn'),
		open_delete = $('.keyword__delete-btn'),
		close = $('.modal-close'),
		container = $('.modal-container'),
		container_add = $('.modal-container.add'),
		container_delete = $('.modal-container.delete');

	//開くボタンをクリックしたらモーダルを表示する
	open_add.on('click',function(){	
		container_add.addClass('active');
		return false;
	});
	open_delete.on('click',function(){	
		container_delete.addClass('active');
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
});