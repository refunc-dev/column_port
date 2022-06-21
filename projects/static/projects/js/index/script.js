$(document).ready(function () {
    $('.projects__favourite').on('click', function () {
		let img = $(this).find('.projects__favourite-image');
		if ( $(this).hasClass('active') ) {
			$(this).removeClass('active')
			img.attr({'src': '/static/projects/images/normal.png'});
		} else {
			$(this).addClass('active')
			img.attr({'src': '/static/projects/images/favourite.png'});
		}
	});

	// 変数に要素を入れる
	var open = $('.projects__add-btn, #new-project'),
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
});