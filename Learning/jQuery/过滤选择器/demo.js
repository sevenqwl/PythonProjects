$(function(){
    // $('li:first').css('background','#ddd');
    // $('li:last').css('background', '#ddd');
    // $('li:not(".red")').css('background', '#ddd');
    // $('li:even').css('background', '#ddd');
    // $('li:odd').css('background', '#ddd');
    // $('li:eq(2)').css('background', '#ddd');
    // $('li:gt(2)').css('background', '#ddd');
    // $('li:lt(2)').css('background', '#ddd');


    // $('li:first-child').css('background','#ddd');
    // $('li:last-child').css('background','#ddd');
    // $('li:only-child').css('background','#ddd');
    // $('li:nth-child(even)').css('background','#ddd');
    // $('li:nth-child(3n)').css('background','#ddd');  // 每隔3倍显示

    // alert($('.red').is('li'));
    // alert($('.red').is('div'));

    // alert($('.red').is(function(){
    //     return $(this).attr('title') == '列表3';  //注意，必须使用$(this)来表示要判断的元素，否则不管function里是否返回true或false都和调用的元素无关
    // }));
    // alert($('.red').eq(0).hasClass('red'))
    $('li').slice(4,6).css('background','#ddd');
    // $('li').slice(2,-2).css('background','#ddd');

    // $('#box').find('li').css('background','#ddd');
    // $('li').filter('.red, :first-child, :last').css('background','#ddd');
    // $('li').filter(function(){
    //     return $(this).attr('class') == 'red' && $(this).attr('title') == '列表3';
    // }).css('background', '#ddd');


});
