$(document).ready(function () {
	// 変数に要素を入れる
	var open_add = $('#add-report'),
		open_delete = $('#settings-report'),
		close = $('.modal-close'),
		container = $('.modal-container'),
		container_add = $('.modal-container.add'),
		container_delete = $('.modal-container.settings'),
		tab = $('.reports__tab-link'),
		item = $('.reports__item');

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
		if (!$(e.target).closest('.modal-body').length) {
			container.removeClass('active');
		}
	});

	tab.on('click',function() {
		tab.removeClass('checked');
		$(this).addClass('checked');
		item.removeClass('display');
		item.removeClass('hidden');

		if ($(this).hasClass('all')) {
			$('.reports__item.all').addClass('display');
		} else if ($(this).hasClass('organic')) {
			$('.reports__item.organic').addClass('display');
		} else if ($(this).hasClass('directory')) {
			$('.reports__item.directory').addClass('display');
		}

		return false;
	})
});