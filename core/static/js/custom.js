jQuery(document).ready(function($){




	/************** Scroll Navigation *********************/
	$('.navigation').singlePageNav({
        currentClass : 'active'
    });

	/************************* 計算寬度大於768才執行WOW動畫 ***********************/
	if($(window).width() >= 768){
		new WOW().init();
	}
	



});