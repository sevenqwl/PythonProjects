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

$(function(){
    $('.panel-footer .btn-toolbar button').click(function(){
        var page = $(this).val();
        
        var pageurl = 'extensions' + '?page=' + page;
        var tr_html, tr_all_html;
        $.get(pageurl, function(data){
            $.each(data, function(i, item){
                console.log(i, item);
                var idnum = i + 1;
                var vfields = item.fields;
                var tr_all_content = "<tr >"
                                +"<td><input type='checkbox' /></td>"
                                +"<td id=''>"+ idnum +"</td>"
                                +"<td id=''>"+ vfields.date +"</td>"
                                +"<td id=''>"+ vfields.time +"</td>"
                                +"<td id=''>"+ vfields.floor +"</td>"
                                +"<td id=''>"+ vfields.model +"</td>"
                                +"<td id=''>"+ vfields.position +"</td>"
                                +"<td id=''>"+ vfields.ip +"</td>"
                                +"<td id=''>"+ vfields.mac +"</td>"
                                +"<td id=''>"+ vfields.sip1 +"</td>"
                                +"<td id=''>"+ vfields.sip1_status +"</td>"
                                +"<td id=''>"+ vfields.sip1_server +"</td>"
                                +"<td id=''>"+ vfields.sip1_outbound +"</td>"
                                +"<td id=''>"+ vfields.sip2 +"</td>"
                                +"<td id=''>"+ vfields.sip2_status +"</td>"
                                +"<td id=''>"+ vfields.sip2_server +"</td>"
                                +"<td id=''>"+ vfields.sip2_outbound +"</td>"
                                +"<td id=''>"+ vfields.update_server +"</td>"
                            +"</tr>";
                var tr_content = "<tr >"
                                +"<td><input type='checkbox' /></td>"
                                +"<td id=''>"+ idnum +"</td>"
                                +"<td id=''>"+ vfields.date +"</td>"
                                +"<td id=''>"+ vfields.time +"</td>"
                                +"<td id=''>"+ vfields.floor +"</td>"
                                +"<td id=''>"+ vfields.ip +"</td>"
                                +"<td id=''>"+ vfields.mac +"</td>"
                                +"<td id=''>"+ vfields.sip1 +"</td>"
                                +"<td id=''>"+ vfields.sip1_status +"</td>"
                                +"<td id=''>"+ vfields.sip1_server +"</td>"
                                +"<td id=''>"+ vfields.sip2 +"</td>"
                                +"<td id=''>"+ vfields.sip2_status +"</td>"
                                +"<td id=''>"+ vfields.sip2_server +"</td>"
                            +"</tr>";
                tr_all_html += tr_all_content;
                tr_html += tr_content;
            });
            $("#extensions_table_all tbody").html(tr_all_html);
            $("#extensions_table tbody").html(tr_html);

        });
    });

    // 展开表格高度
    $('.panel-footer .fa').on('click', function(){
        var ele = $('#main_panel');
        var defaultHeight = "480px";
        var autoHeight = ele.css('height', 'auto').height();
        if ($(this).hasClass('fa-chevron-circle-down')){
            ele.animate({height: autoHeight}, 500);
            $(this).removeClass('fa-chevron-circle-down').addClass('fa-chevron-circle-up');
        }else{
            ele.animate({height: defaultHeight}, 500);
            $(this).removeClass('fa-chevron-circle-up').addClass('fa-chevron-circle-down');
        }
    });
});
