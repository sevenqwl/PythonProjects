/**
 * Created by Seven on 2017/8/31.
 */



//for csrf
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
//end csrf

//global chat record dic
GLOBAL_CHAT_RECORD_DIC = {
    'single': {},
    'group': {},
}

$(document).ready(function () {
    //set csrf before send ajax
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    //end set csrf

    // 定时取消息
// {#        var MsgRefresher = setInterval(function(){#}
// {#            GetNewMsgs();#}
// {#        }, 3000);#}
    username = $('#username').text();
    user_id = $('#username').attr('user-id');
    user_head_img = $("#user-head-img").attr('src');
    user_head_img_str = user_head_img.split('/');
    user_head_img_name = user_head_img_str[user_head_img_str.length - 1];
    console.log(user_head_img);
    console.log(user_head_img_name);


    GetNewMsgs(); //开始去取消息

    $("#navbar a[href='{{ request.path }}']").parent().addClass('active');
    // send msg
    $("body").delegate("#saytext", "keydown", function(e){
       if(e.which == 13) {  //Enter key down
           if(e.ctrlKey){
               console.log("ctrl+enter");
               var msg_content = $("#saytext").val() + '\n';
               $("#saytext").val(msg_content);

           }else{
               e.preventDefault();
               e.stopPropagation();
               // send msg button clicked，调用发送按钮函数
               $("#send-btn").click();
               return false;

           }
       }
    });
    // 发送按钮函数
    $("#send-btn").click(function(){
        var msg_content = $("#saytext").val();
        if ($.trim(msg_content).length > 0){
            SendMsg(msg_content);
            //no wait the send_msg's call confirm msg
            AddSentMsgIntoBox(msg_content,'text');
            $("#saytext").val("").focus();
        }
    });

}); // end doc ready
// 发送文本消息
function SendMsg(msg_content){
    var contact_id = $("#chat_box_title_user").attr("contact-id");
    var contact_type = $("#chat_box_title_user").attr("contact-type");
    var msg_type = "text";
    if (contact_id && contact_type){
        var msg_item = {
            'from_user_id': user_id,
            'from_name': username,
            'to_user_id': contact_id,
            'contact_type': contact_type,
            'msg_content': msg_content,
            'msg_type':　msg_type,
            'head_img': user_head_img_name,
        }
        console.log(msg_item);
        $.post("/webchat/msg_send/",{data:JSON.stringify(msg_item)},function(callback){
            console.log(callback);
        });
    } // end if
}


function AddSentMsgIntoBox(msg_content,msg_type){
    if ($('#chat_box_title_user').attr('contact-type') != "" && $('#chat_box_title_user').attr('contact-id') != ""){
        if (msg_type == "text") {
            var new_msg_ele =   "<li class='chat-mine'>" +
                                    "<div class='chat-user'>" +
                                        "<img src=" + user_head_img + ">" +
                                        "<cite>" +
                                            "<i>" + new Date().toLocaleTimeString() + "</i>" +
                                            username +
                                        "</cite>" +
                                    "</div>" +
                                    "<div class='chat-text'>" +
                                        replace_em(msg_content) +
                                    "</div>" +
                                "</li> ";

        } else if (msg_type.indexOf('image') == 0) {
            var new_msg_ele =  "<li class='chat-mine'>" +
                                    "<div class='chat-user'>" +
                                        "<img src=" + user_head_img + ">" +
                                        "<cite>" +
                                            "<i>" + new Date().toLocaleTimeString() + "</i>" +
                                            username +
                                        "</cite>" +
                                    "</div>" +
                                    "<div class='chat-img'><img src='/static/images/uploads/" +
                                     user_id + "/" + msg_content + "' /></div>" +
                                    "</div>" +
                                "</li> ";

        } else {
            var new_msg_ele =   "<li class='chat-mine'>" +
                                    "<div class='chat-user'>" +
                                        "<img src=" + user_head_img + ">" +
                                        "<cite>" +
                                            "<i>" + new Date().toLocaleTimeString() + "</i>" +
                                            username +
                                        "</cite>" +
                                    "</div>" +
                                    "<div class='chat-text'>" +
                                        "<div class='file-item'>" +
                                            "<div class='file-item-header'>" +
                                                "<img src='/static/images/utils/filefolder.png'>" +
                                                    msg_content +
                                            "</div>" +
                                            "<a href='/static/images/uploads/" + user_id + "/" + msg_content + "' target='_blank' download='" + msg_content + "' >" +
                                                "<span>文件发送成功！！！</span>" +
                                            "</a>" +
                                        "</div>" +
                                    "</div>" +
                                "</li> ";



        }
    }

    $("#box_window ul").append(new_msg_ele);




    // $("#box_window").scrollTop($("#box_window")[0].scrollHeight);
    $("#box_window").animate({scrollTop: $(".chat-box-window")[0].scrollHeight}, 500);
}

$(function(){
    $("#left_contact_panel .tab .tab-item a").click(function () {
        $(this).parent().siblings().find('a').removeClass('active-tab');
        $(this).addClass('active-tab');
        $("#left_contact_panel .tab-content li").removeClass('activeddd');

    });
    $("#right_statements_panel .tab .tab-item a").click(function () {
        $(this).parent().siblings().find('a').removeClass('active-tab');
        $(this).addClass('active-tab');
        $("#right_statements_panel .tab-content li").removeClass('activeddd');

    });


    // 点击左侧栏用户、组
    $('#left_contact_panel li').on('click',function () {
        var $chat_box_title_user = $('#chat_box_title_user');
        $(this).addClass('activeddd');
        $(this).siblings().removeClass('activeddd');
        var contact_id = $(this).attr('contact-id');
        var contact_name = $(this).find('.contact-name').text();
        var contact_type = $(this).attr('contact-type');

        console.log(contact_id,contact_name,contact_type);

        // 在切换前把当前的聊天记录归档
        var current_session_id = $chat_box_title_user.attr('contact-id');
        var current_session_type = $chat_box_title_user.attr('contact-type');
        if (current_session_id.length){  // has session
            GLOBAL_CHAT_RECORD_DIC[current_session_type][current_session_id] = $('.chat-box-window ul').html();
        }

        var chat_box_title_content = contact_name;
        $chat_box_title_user.html(chat_box_title_content);
        $chat_box_title_user.attr('contact-id', contact_id);
       $chat_box_title_user.attr('contact-type', contact_type);
        $('.contact-content-history').removeClass('hidden');

        var new_contact_chat_record = GLOBAL_CHAT_RECORD_DIC[contact_type][contact_id];
        if (typeof new_contact_chat_record == 'undefined'){
            new_contact_chat_record = '';
        }
        $('.chat-box-window ul').html(new_contact_chat_record);
        $('#box_window').animate({scrollTop: $('.chat-box-window')[0].scrollHeight}, 'fast');

        // 取消提示消息
        var contact_ele = $(".list-group li[contact-type='" + contact_type + "']").filter("li[contact-id='" + contact_id + "']")[0];
        var current_new_msg_num = $(contact_ele).find('.badge').text(0);
        $(contact_ele).find('.badge').addClass('hidden');
    });

});


function GetNewMsgs() {
    console.log('获取新消息中');
    $.getJSON("/webchat/new_msgs/", function(callback){
        if (callback != ""){
            ParseNewMsgs(callback); // 把新消息进行解析
        }
        return GetNewMsgs();  // 递归自己
    });
}


function ParseNewMsgs(callback) {
    var current_session_type = $("#chat_box_title_user").attr("contact-type");
    var current_session_id = $("#chat_box_title_user").attr('contact-id');
    console.log('正在ParseNewMsgs');
    console.log(callback);
    for (var i in callback) {
        console.log(callback[i]);
        var from_user_id = callback[i].from_user_id
        var msg_type = callback[i].msg_type;
        var msg_content = callback[i].msg_content;
        if (callback[i].contact_type == 'single') {
            var msg_from_contact_id = callback[i]['from_user_id'];
        } else {
            var msg_from_contact_id = callback[i]['to_user_id'];
        }

        if (msg_type == "text") {
            var msg_item_ele = "<li>" +
                                    "<div class='chat-user'>" +
                                        "<img src=/static/images/headimg/" + callback[i]['head_img'] + ">" +
                                        "<cite>" +
                                            callback[i]['from_name'] +
                                            "<i>" + callback[i].timestamp + "</i>" +
                                        "</cite>" +
                                    "</div>" +
                                    "<div class='chat-text'>" +
                                    replace_em(callback[i].msg_content) +
                                    "</div>" +
                                "</li> "

        } else if (msg_type.indexOf('image') == 0) {
            file_src = msg_content.replace(/^media/, '/static');
            var msg_item_ele = "<li>" +
                                    "<div class='chat-user'>" +
                                        "<img src=/static/images/headimg/" + callback[i]['head_img'] + ">" +
                                        "<cite>" +
                                            callback[i]['from_name'] +
                                            "<i>" + callback[i].timestamp + "</i>" +
                                        "</cite>" +
                                    "</div>" +
                                    "<div class='chat-img'><img src='" + file_src +
                                    "' /></div>" +
                                    "</div>" +
                                "</li> "

        } else {
            file_src = msg_content.replace(/^media/, '/static');
            file_name = msg_content.split('/').slice(-1)
            var msg_item_ele = "<li>" +
                                    "<div class='chat-user'>" +
                                        "<img src=/static/images/headimg/" + callback[i]['head_img'] + ">" +
                                        "<cite>" +
                                            callback[i]['from_name'] +
                                            "<i>" + callback[i].timestamp + "</i>" +
                                        "</cite>" +
                                    "</div>" +
                                    "<div class='chat-text'>" +
                                        "<div class='file-item'>" +
                                            "<div class='file-item-header'>" +
                                                "<img src='/static/images/utils/filefolder.png'>" +
                                                    file_name +
                                            "</div>" +
                                            "<a href='" + file_src + "' target='_blank' download='" + file_name + "' >" +
                                                "<span>文件接收成功，点击下载！！！</span>" +
                                            "</a>" +

                                        "</div>" +
                                    "</div>" +
                                "</li> "

        }

        if (msg_from_contact_id == current_session_id && current_session_type == callback[i].contact_type) {
            // 此消息的发送方当前正在跟我聊天

            $("#box_window ul").append(msg_item_ele);
            $("#box_window").animate({scrollTop: $(".chat-box-window")[0].scrollHeight}, 500);
        } else {
            // 此消息发送者当前没打开聊天框，消息暂存内存
            if (GLOBAL_CHAT_RECORD_DIC[callback[i].contact_type][msg_from_contact_id]) {
                GLOBAL_CHAT_RECORD_DIC[callback[i].contact_type][msg_from_contact_id] += msg_item_ele;
            } else {
                GLOBAL_CHAT_RECORD_DIC[callback[i].contact_type][msg_from_contact_id] = msg_item_ele;
            }

            // 新消息提醒
            var contact_ele = $(".list-group li[contact-type='" + callback[i].contact_type + "']").filter("li[contact-id='" + msg_from_contact_id + "']")[0];

            var current_new_msg_num = $(contact_ele).find(".badge").text();
            $(contact_ele).find('.badge').removeClass('hidden');
            $(contact_ele).find('.badge').text(parseInt(current_new_msg_num) + 1);


        }
    }

}

// 文件上传加载函数

function OpenFileUploadBox(){
    $('#file_upload').trigger("click");
}
function GetFilePath(){
    // console.log($('#file_upload')[0].files[0]);
    var file_data = $('#file_upload')[0].files[0];
    console.log(file_data);
    var file_type = file_data['type'];

    var contact_id = $("#chat_box_title_user").attr("contact-id");
    var contact_type = $("#chat_box_title_user").attr("contact-type");
    var msg_data = {
            'from_user_id': user_id,
            'from_name': username,
            'to_user_id': contact_id,
            'contact_type': contact_type,
            'msg_type': file_type,
            'head_img': user_head_img_name,
    }
    msg_data = JSON.stringify(msg_data);
    FileUpload(msg_data, file_data);

}

function FileUpload(msg_data, file_data){
    var formData = new FormData();  // 生成一个form表单
    // file_item = $('#file_upload')[0].files[0];
    // file_type = file_item['type'];
    formData.append('file_data', file_data);
    formData.append('msg_data', msg_data);

    $.ajax({
        url: "/webchat/file_upload/",
        type: 'POST',
        data: formData,
        processData: false,  // tell jQuery not to process the data
        contentType: false,  // tell jQuery not to set contenyType
        success: function(data){
            console.log(data);
        }
    }); // end ajax

    // 清空file_upload文本域
    var file = $("#file_upload");
    file.after(file.clone().val(""));
    file.remove();

    GetFileUploadProgress(file_data);
    $(".progress").removeClass('hidden');
}

function GetFileUploadProgress(file_obj){

    var file_progress = "<div id='file-progress' class='progress' style='width:200px;right: 0px;top:5px;margin-top:5px;margin-left: 305px;'>" +
                    "<div class='progress-bar progress-bar-success progress-bar-striped'  role='progressbar' aria-valuenow='40' aria-valuemin='0' aria-valuemax='100' style='width: 0%'>" +
                        "0%" +
                    "</div>" +
                "</div>";
    $("#box_window ul").append(file_progress);


    var UploadProcessRefresh = setInterval(function(){
        $.getJSON("/webchat/file_upload_progress/", {filename: file_obj.name}, function(callback){
            console.log("upload progress:" + callback.recv_size);
            if (file_obj.size == callback.recv_size){
                // upload done
                clearInterval(UploadProcessRefresh);
                $.get("/webchat/delete_cache_key/", {cache_key: file_obj.name}, function(callback){
                    console.log(callback);
                });
                AddSentMsgIntoBox(file_obj.name,file_obj.type);

                setTimeout(function(){
                    $('#file-progress').remove();
                },1000);
            }
            var current_percent = (callback.recv_size/file_obj.size)*100 + "%";
            $(".progress-bar").css("width", current_percent);
            $(".progress-bar").text(current_percent);
        });
    }, 1000);
}

// 文件上传加载函数 end

// QQ表情
$(function(){
    $('.emotion').qqFace({
        assign:'saytext', //给输入框赋值
        path:'/static/images/emoj/face/'    //表情图片存放的路径
    });
});


function replace_em(msg_content){
    msg_content = msg_content.replace(/</g,'< ');
    msg_content = msg_content.replace(/>/g,' >');
    msg_content = msg_content.replace(/\n/g,'<br/>');
    msg_content = msg_content.replace(/\r/g,'<br/>');
    msg_content = msg_content.replace(/\[em_([0-9]*)\]/g,'<img src="/static/images/emoj/face/$1.gif" border="0" />');
    return msg_content;
}

// 插入话术到 textarea 并自动获得焦点
$(document).ready(function(){
    $('#statements-tab ul li').click(function(e) {
        var msg_content = $(this).text();
        if(e.ctrlKey){
            var msg_content = $("#saytext").val() + "  " + msg_content;
        }
        if(e.shiftKey){
            var msg_content = $("#saytext").val() + "\n" + msg_content;
        }

        $('#saytext').val(msg_content).focus();  // 插入话术并自动获得焦点
        // $('#send-btn').trigger('click');  // 触发点击发送按钮

    });
});

// 搜索框模糊匹配查询
$(document).ready(function(){
    $('#search_window').bind('input propertychange', function(){
        var current_val = $('#search_window input').val();

        if (current_val == ""){
            // 输入框内容为空则显示默认列表信息
            $('.right-statements-panel .statements-list li').removeClass('hidden');
            $('.search-close-icon').addClass('hidden');

        }else{
            for (var i = 0; i < $('.right-statements-panel .statements-list li').length; i++) {
                if ($('.right-statements-panel .statements-list li').eq(i).text().toUpperCase().indexOf(current_val.toUpperCase()) != -1){
                    $('.right-statements-panel .statements-list li').eq(i).removeClass('hidden');
                }else{
                    $('.right-statements-panel .statements-list li').eq(i).addClass('hidden');
                }
            }
            $('.search-close-icon').removeClass('hidden');
            $(this).find('input').attr('title', current_val);
            console.log($(this).find('input'));

            $('.search-close-icon').click(function () {
                $('#search_window input').val("");
                $('.search-close-icon').addClass('hidden');
                $('.right-statements-panel .statements-list li').removeClass('hidden');
                $('#search_window input').attr('title', '');
            })
        }

    });

});

// 聊天框中点击图片放大
// function OpenExtendImg(){
//     var img_url = $(".chat-img img").attr("src");
//     console.log("extend pic");
//     $(".chat-modal-backdrop").removeClass("hidden");
//     $(".chat-extend-img-box img").attr("src", img_url);
//     $(".chat-extend-img-box").removeClass("hidden");
// }

$(function(){

    $("#box_window").delegate(".chat-img img", "click", function(){
        var img_url = $(this).attr("src");
        $(".chat-extend-img-box img").attr("src", img_url);
        $("#chat-modal-img").removeClass("hidden");
        var img_height = $('.chat-extend-img').height();
        var img_width =  $('.chat-extend-img').width();
        var close_window_height = 80;
        var close_window_width = 80;

        var newPos = new Object();
        if ($(window).width() > img_width) {
            newPos.left = ($(window).width() - img_width) / 2;
        }else{
            newPos.left = 0;
        }
        if ($(window).height()-160 > img_height) {
            newPos.top = ($(window).height() - img_height) / 2;
        }else {
            newPos.top = 80;
        }
        var currentTop = $(window).scrollTop();
        if (currentTop > 0){
            newPos.top = currentTop +100;
        }

        $('.chat-extend-img').offset(newPos);  // 图片居中显示
        $('.chat-close-window').offset({top: newPos.top-30,left: newPos.left + img_width -30});

        // 窗口滚动条变化时图片显示位置
        window.onscroll = function(){
            var currentTop = $(window).scrollTop();
            console.log(11)
            if (currentTop > 0){
                var newPos = new Object();

                if ($(window).width() > img_width) {
                    newPos.left = ($(window).width() - img_width) / 2;
                }else{
                    newPos.left = 0 +currentTop;
                }
                if ($(window).height()-160 > img_height) {
                    newPos.top = ($(window).height() - img_height) / 2;
                }else {
                    newPos.top = 80 +currentTop;
                }

                $('.chat-extend-img').offset(newPos);  // 图片居中显示
                $('.chat-close-window').offset({top: newPos.top-30,left: newPos.left + img_width -30});

            }
        }

        // 窗口size变化时图片显示位置
        $(window).resize(function(){
            var newPos = new Object();

            if ($(window).width() > img_width) {
                newPos.left = ($(window).width() - img_width) / 2;
            }else{
                newPos.left = 0;
            }
            if ($(window).height()-160 > img_height) {
                newPos.top = ($(window).height() - img_height) / 2;
            }else {
                newPos.top = 80;
            }

            $('.chat-extend-img').offset(newPos);  // 图片居中显示
            $('.chat-close-window').offset({top: newPos.top-30,left: newPos.left + img_width -30});

        });


    });

    $("#chat-modal-img .chat-close-window").click(function(){
        $("#chat-modal-img").addClass("hidden");
    });

});

// 获取ping结果
$(function(){
    $('#get_ping_result').mouseover(function(){
        var interval_ping = setInterval(get_ping_result, 1000);
        $('#get_ping_result').mouseout(function(){
            console.log('quxiuao ');
            clearInterval(interval_ping);
        });
    });

    function get_ping_result(){
        $.getJSON("/webchat/get_ping_result", function(callback){
            var ping_result = callback;
            var get_ping_obj = $('#get_ping_result')
            get_ping_obj.html('');
            $.each(ping_result, function(i, val){
                ping_result = val + "</br>";
                get_ping_obj.append(ping_result);
            });
            get_ping_obj.animate({scrollTop: get_ping_obj[0].scrollHeight}, 500);
        });
    }
});

// 倒计时
$(function(){
   $('#countdown').on('click', function(){
       var count = 10;
       var countdown_intervarl = setInterval(function () {
           $('#countdown input').val(count);
           count -= 1;
           console.log(count);
           if (count == -1) {
               clearInterval(countdown_intervarl);
           }

       }, 1000);

   });

});