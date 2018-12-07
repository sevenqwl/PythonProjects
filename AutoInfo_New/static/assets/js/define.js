/**
 * Created by Seven on 2018/2/2.
 */

// 返回顶部
function GoTop(){
    $('html, body').animate({scrollTop: 0}, 500);
}
$(function(){
    $(window).on('scroll',function(){
        var currentTop = $(window).scrollTop();
        if (currentTop>100){
            $('.go-top').removeClass('hide');
        }else{
            $('.go-top').addClass('hide');
        }
    });
});