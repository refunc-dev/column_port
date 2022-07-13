$(document).ready(function () {
	// 変数に要素を入れる
	var open_keyword = $('#add-keyword'),
		open_remove = $('#remove-article'),
		close = $('.modal-close'),
		container = $('.modal-container');
		container_keyword = $('.modal-container.add-keyword');
		container_remove = $('.modal-container.remove-article');

	//開くボタンをクリックしたらモーダルを表示する
	open_keyword.on('click',function(){	
		container_keyword.addClass('active');
		return false;
	});

	open_remove.on('click',function(){	
		container_remove.addClass('active');
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