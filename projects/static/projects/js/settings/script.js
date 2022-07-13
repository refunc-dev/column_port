$(document).ready(function () {
	// 変数に要素を入れる
	var open_member = $('#add-member'),
		open_competitor = $('#add-competitor'),
		open_project = $('#delete-project'),
		close = $('.modal-close'),
		container = $('.modal-container');
		container_member = $('.modal-container.add-member');
		container_competitor = $('.modal-container.add-competitor');
		container_project = $('.modal-container.delete-project');

	//開くボタンをクリックしたらモーダルを表示する
	open_member.on('click',function(){	
		container_member.addClass('active');
		return false;
	});

	open_competitor.on('click',function(){	
		container_competitor.addClass('active');
		return false;
	});

	open_project.on('click',function(){	
		container_project.addClass('active');
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