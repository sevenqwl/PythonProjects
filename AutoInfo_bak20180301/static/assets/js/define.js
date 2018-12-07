/**
 * Created by Seven on 2018/2/2.
 */

function GoTop(){
    // $(window).scrollTop(0);
     $('#main-content').animate({scrollTop: 0}, 500);
}
$(function(){
    $('#main-content').onscroll = function(){
        var currentTop = $('#main-content').scrollTop();
        if (currentTop>500){
            $('.go-top').removeClass('hide');
        }else{
            $('.go-top').addClass('hide');
        }
    }
});