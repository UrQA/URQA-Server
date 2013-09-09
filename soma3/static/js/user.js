var resizeStatusPopupMemberJoin = false,
	resizeStatusPopupNotification = false,
	resizeStatusPopupInformation = false,
	resizeStatusPopupEventpath = false.
	resizeStatusPopupLd = false,
	resizeStatusCreateProject = false,
	resizeStatusLoginBox = false,
	resizeStatusProjectList = false,
	resizeStatusConfirm = false;

var variables = $().loadVariableFile("./css/theme/dark");

function confirmCancel()
{
	hideConfirm();
}
function confirmProcess()
{
	if($("#warning-alert").css("display", "block") )
    {
        $.ajax({
          type: 'get'
        , url: '/urqa/project/' + project_id + '/delete'
        , success :  function()
            {
                document.location = "/urqa/projects";
            }
        })

    }

}
//modifiproject
function modifiProject(obj)
{
	var e = obj.elements;

    //projectname
    var projectname = e[0].value
    //platform
    var platform = ''
    var platformlist =  $('#platform_list').find('li').toArray()
    for(var i = 0 ; i < platformlist.length ; i++)
    {
        if(platformlist[i].getAttribute('data-value') == 'true')
            platform = platformlist[i].innerText
    }
    //category
    var category= ''
    var categorylist =  $('#category_list').find('li').toArray()
    for(var i = 0 ; i < categorylist.length ; i++)
    {
        if(categorylist[i].getAttribute('data-value')== 'true')
            category = categorylist[i].innerText
    }
    //stage
    var stage = ''
    var stagelist =  $('#stage_list').find('li').toArray()
    for(var i = 0 ; i < stagelist.length ; i++)
    {
        if(stagelist[i].getAttribute('data-value')== 'true')
            stage = stagelist[i].innerText
    }
    //timezone
    var timezone = ''
    var timezonelist =  $('#timezone_list').find('li').toArray()
    for(var i = 0 ; i < timezonelist.length ; i++)
    {
        if(timezonelist[i].getAttribute('data-value')== 'true')
            timezone = timezonelist[i].innerText
    }

    //data create
    var data = { "projectname" : projectname , "platform" : platform, "category" : category, "stage" : stage, "timezone" : timezone }

    var csrftoken = getCookie('csrftoken')
    $.ajax({
      type: 'post'
    , url: '/urqa/project/'+ project_id +'/modify'
    , beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }}
    , data: data
    , success : function(data) {
             if(data['success'])
                 document.location = "/urqa/project/" + project_id
             else
                alert(data['message'])
        }
    })

	hidePopupModifyProject();

	return false;
}

function createProject(obj)
{
	var e = obj.elements;

	if(e["appname"].value == "")
	{
		$(e["appname"]).addClass("error");
        return false;
	}

    var platformlist = $('#app_platform_list').find('li').toArray()
    var platformdata = ''
    for (var i = 0; i< platformlist.length ; i++)
    {
        var platform = platformlist[i]
        if(platform.getAttribute('data-value') == 'true'){
            platformdata  = platform.innerText
            break;
        }

    }

    //추가 ajax
    var categorylist = $('#app_category_list').find('li').toArray()
    var categorydata = ''
    for (var i = 0; i< categorylist.length ; i++)
    {
        var category = categorylist[i]
        if(category.getAttribute('data-value') == 'true'){
            categorydata  = category.innerText
            break;
        }

    }

    var stagelist = $('#app_stage_list').find('li').toArray()
    var stagedata = ''
    for (var i = 0; i< stagelist.length ; i++)
    {
        var stage = stagelist[i]
        if(stage.getAttribute('data-value') == 'true'){
            stagedata  = stage.innerText
            break;
        }

    }

    var data = {'name' : '', 'platform' : '' , 'stage' : '' , 'category':''}
    data['name'] = e["appname"].value
    data['platform'] = platformdata
    data['stage'] = stagedata
    data['category'] = categorydata


     var csrftoken = getCookie('csrftoken')
     $.ajax({
      type: 'post'
    , url: '/urqa/project/registration'
    , beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }}
    , data: data
    , success : function(data) {
             if(data['success'])
                successCreateProject(data['prjname'],data['apikey'],data['color'],data['platform'])
        }
    })

	return false;
}
function successCreateProject(prjname,apikey,color,platform)
{
    platform = platform.toLowerCase()
	var device = (data['platform'] == 1 ? "iphone" : "android");
    hidePopupCreateProject();
    $("#project-list > .list").append("<div>                                                                    \
                    <a href= \"/urqa/project/"+ apikey + "\">                                                   \
                        <div></div>                                                                                \
                        <div class=\"" + platform + "\"></div>                                                       \
                        <span></span>                                                                               \
                        <p class=\"" + color+ "\"><span>ERROR</span>0</p>                                         \
                    </a>                                                                                             \
                        <label onclick=\"copyThis(this)\">" + prjname + "<span>" + apikey + "</span></label>   \
                </div>                                                                                               \
                ");

    //$("#project-list > .list").append("<a href= \"/urqa/project/" + apikey + "\"><div><div></div><div class=\""+ platform + "\"></div><span></span><p class=\"" + color + "\"><span>ERROR</span>0</p><label>" + prjname + "<span>" +apikey+ "</span></label></div></a>");

    var chd = $("#project-list > .list > a:nth-last-child(1) > div");

    resizeProjectList();

    chd.css({"margin-top": "-30px", opacity: 0.0});
    chd.delay(250).animate({
        "margin-top": 0,
        opacity: 1.0
    }, 250, function(){
        chd.css({"margin-top": 0, opacity: 1.0});
    });

    //새로 만들어진 프로젝트 복사 되게 추가
    copyToClipboard("#project-list > .list > div > label > span", copyThis);
}
function submitViewer(event, obj)
{
 	if(event.keyCode == 13)
	{
		if(isValidEmail(obj.value) == false)
		{
			alert("정상적인 이메일 주소가 아닙니다.");
			obj.value = "";
		}
		else
		{
            var username = obj.value
            var data  = {'username' : username}

            var csrftoken = getCookie('csrftoken')
            $.ajax({
              type: 'post'
            , url: '/urqa/project/'+project_id +'/viewer/registration'
            , beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }}
            , data: data
            , success : function(data) {
                    if(data["success"])
                    {
                        $('#addviewer').before("<tr><td class=\"float\"><p>" + data['username'] + "</p></td><td><div class=\"button red event\" onclick = \"deleteviewer(this)\" data-name=\"Remove\" style=\"width: 74px; height: 26px; margin: 2px;\"></div></td></tr>");
                        $('#addviewer').children().children().value = "";
                        tableResizing();
                        $('#addviewer').parent().parent().parent().parent().scrollTop( $('#addviewer').position().top);
                    }
                    else
                    {
                        alert(data['message'])
                    }
                }
            })
		}
	}
}
function submitComment(event, obj)
{
	if(event.keyCode == 13)
	{
		var chd = $(obj).parent().parent().parent().children(":nth-last-child(2)");
		chd.before("<tr><td class=\"float\"><img src=\"" + $(".navbar-profile > .profile > img").attr("src") + "\" /></td><td class=\"float\"><p>" + $("#profile-menu > .color > .text > .name").html() + "</p><p>" + obj.value + "</p></td><td>" + new Date().format("yyyy/MM/dd") + "</td></tr>");
		obj.value = "";
		tableResizing();
	}
}
function copyThis(obj)
{
	return $(obj).html().replace(/[<][^>]*[>]/gi, "");
}
function openNotification()
{
	$("#popup-notification > div").css({height: "", "padding-top": "", "padding-bottom": ""} );
	$("#popup-notification > div > span").css({display: ""});
	$("#popup-notification > div").show();
	$("#popup-notification").show();
}
function newNotification(title, content, href)
{
	$("#profile-menu > div:nth-last-child(1) > div > span:nth-child(2) > .notification").attr("data", $("#popup-notification > div").length + 1);
	$("#popup-notification").append("<div data-href=\"" + href + "\"><span></span><label>" + title + "</label><p>" + content + "</p></div>");
	var chd = $("#popup-notification > div:nth-last-child(1)");
	var h = chd.height();
	chd.css({"padding-top": 0, "padding-bottom": 0, "height": 0} );
	chd.animate({
		"padding-top": 14,
		"padding-bottom": 14,
		"height": h
	}, 250, function(){
		$(this).css({"padding-top": 14, "padding-bottom": 14, "height": h})
	});

	chd.click(function(){
		if(bodyChecker_noti == false)
		{
			document.location = $(this).attr("data-href");
		}
		else
		{
			$(this).children("span").hide();
			$(this).animate({
				height: 0,
				"padding-top": 0,
				"padding-bottom": 0
			}, 250, function(){
				$(this).hide();
				$(this).addClass("read");
				$("#profile-menu > div:nth-last-child(1) > div > span:nth-child(2) > .notification").attr("data", $("#popup-notification > div:not(.read)").length);
				if($("#popup-notification > div:visible").length == 0)
					$("#popup-notification").hide();
			});
		}
		bodyChecker_noti = false;
	});
	chd.children("span").click(function(){ bodyChecker_noti = true; });

	$("#popup-notification").show();
	resizePopupNotification();
}
function tableResizing()
{
    $("table > tbody > tr.empty").each(function(){
        $(this).css("display", "table-row");
        $(this).children().each(function(child){
            if($(this).attr("data-match") != "true")
                return;

            $(this).parent().parent().children().each(function(){
                if($(this).parent().hasClass("empty") == true)
                    return;

                $(this).children().eq(child).children("p").width("1px");
            });

            var w = $(this).width();
            var chd = $(this).parent().parent().children().eq(0).children().eq($(this).index()).children(":not(p)");
            for(var i = 0; i < chd.length; i ++)
            {
                if(chd.eq(i).css("float") != "none")
                    w -= chd.eq(i).width() + 12;
            }

            $(this).parent().parent().children().each(function(){
                if($(this).parent().hasClass("empty") == true)
                    return;

                $(this).children().eq(child).children("p").width(w);
                //여기 임의로 추가...
                if( $(this).children().eq(child).children("p").attr('id') == 'chart')
                {
                    sankeywidth = w;
                    if(sankeyloading)
                        sankeyredraw(sankeydata)
                }
			});
		});
		$(this).css("display", "none");
	});
}
function resizeConfirm()
{
	if($("#warning-alert") )
	{
		var tops = ($(window).height() - $("#warning-alert > .body").height()) / 2;
		var lefts = ($(window).width() - $("#warning-alert > .body").width()) / 2;
		if(resizeStatusConfirm)
		{
			$("#warning-alert > .body").stop(true, true);
			$("#warning-alert > .body").animate({'top': tops, 'left': lefts}, 250, function() { $(this).css({'top': tops, 'left': lefts}); } );
		}
		else
		{
			$("#warning-alert > .body").css({'top': tops, 'left': lefts});
		}
		resizeStatusConfirm = true;
	}
}
function resizePopupMemberjoin()
{
	if($("#popup-memberjoin") )
	{
		var tops = ($(window).height() - $("#popup-memberjoin > .body").height()) / 2;
		var lefts = ($(window).width() - $("#popup-memberjoin > .body").width()) / 2;
		if(resizeStatusPopupMemberJoin)
		{
			$("#popup-memberjoin > .body").stop(true, true);
			$("#popup-memberjoin > .body").animate({'top': tops, 'left': lefts}, 250, function() { $(this).css({'top': tops, 'left': lefts}); } );
		}
		else
		{
			$("#popup-memberjoin > .body").css({'top': tops, 'left': lefts});
		}
		resizeStatusPopupMemberJoin = true;
	}
}
function resizePopupNotification()
{
	if($("#popup-notification") )
	{
		var tops = ($(window).height() - $("#popup-notification").height()) / 2;
		var lefts = ($(window).width() - $("#popup-notification").width()) / 2;
		if(resizeStatusPopupNotification)
		{
			$("#popup-notification").stop(true, true);
			$("#popup-notification").animate({'top': tops, 'left': lefts}, 250, function() { $(this).css({'top': tops, 'left': lefts}); } );
		}
		else
		{
			$("#popup-notification").css({'top': tops, 'left': lefts});
		}
		resizeStatusPopupNotification= true;
	}
}
function resizePopupInformation()
{
	if($("#popup-information") )
	{
		var tops = ($(window).height() - $("#popup-information > .body").height()) / 2;
		var lefts = ($(window).width() - $("#popup-information > .body").width()) / 2;
		if(resizeStatusPopupInformation)
		{
			$("#popup-information > .body").stop(true, true);
			$("#popup-information > .body").animate({'top': tops, 'left': lefts}, 250, function() { $(this).css({'top': tops, 'left': lefts}); } );
		}
		else
		{
			$("#popup-information > .body").css({'top': tops, 'left': lefts});
		}
		resizeStatusPopupInformation = true;
	}
}
function resizePopupEventpath()
{
	if($("#popup-eventpath") )
	{
		var tops = ($(window).height() - $("#popup-eventpath > .body").height()) / 2;
		var lefts = ($(window).width() - $("#popup-eventpath > .body").width()) / 2;
		if(resizeStatusPopupEventpath)
		{
			$("#popup-eventpath > .body").stop(true, true);
			$("#popup-eventpath > .body").animate({'top': tops, 'left': lefts}, 250, function() { $(this).css({'top': tops, 'left': lefts}); } );
		}
		else
		{
			$("#popup-eventpath > .body").css({'top': tops, 'left': lefts});
		}
		resizeStatusPopupEventpath = true;
	}
}
function resizePopupLogdata()
{
	if($("#popup-logdata") )
	{
		var tops = ($(window).height() - $("#popup-logdata > .body").height()) / 2;
		var lefts = ($(window).width() - $("#popup-logdata > .body").width()) / 2;
		$("#popup-logdata > .body").stop(true, true);
		$("#popup-logdata > .body").animate({'top': tops, 'left': lefts}, 250, function() { $(this).css({'top': tops, 'left': lefts}); } );
	}
}
function resizeModifyProject()
{
	if($("#popup-modifyproject") )
	{
		var tops = ($(window).height() - $("#popup-modifyproject > .body").height()) / 2;
		var lefts = ($(window).width() - $("#popup-modifyproject > .body").width()) / 2;
		if(resizeStatusCreateProject)
		{
			$("#popup-modifyproject > .body").stop(true, true);
			$("#popup-modifyproject > .body").animate({'top': tops, 'left': lefts}, 250, function() { $(this).css({'top': tops, 'left': lefts}); } );
		}
		else
		{
			$("#popup-modifyproject > .body").css({'top': tops, 'left': lefts});
		}
		resizeStatusCreateProject = true;
	}
}
function resizeCreateProject()
{
	if($("#popup-createproject") )
	{
		var tops = ($(window).height() - $("#popup-createproject > .body").height()) / 2;
		var lefts = ($(window).width() - $("#popup-createproject > .body").width()) / 2;
		if(resizeStatusCreateProject)
		{
			$("#popup-createproject > .body").stop(true, true);
			$("#popup-createproject > .body").animate({'top': tops, 'left': lefts}, 250, function() { $(this).css({'top': tops, 'left': lefts}); } );
		}
		else
		{
			$("#popup-createproject > .body").css({'top': tops, 'left': lefts});
		}
		resizeStatusCreateProject = true;
	}
}
function resizePopupSymbolUpload()
{
	if($("#popup-uploadsymbol") )
	{
		var tops = ($(window).height() - $("#popup-uploadsymbol > .body").height()) / 2;
		var lefts = ($(window).width() - $("#popup-uploadsymbol > .body").width()) / 2;
		if(resizeStatusLoginBox)
		{
			$("#popup-uploadsymbol > .body").stop(true, true);
			$("#popup-uploadsymbol > .body").animate({'top': tops, 'left': lefts}, 250, function() { $(this).css({'top': tops, 'left': lefts}); } );
		}
		else
		{
			$("#popup-uploadsymbol > .body").css({'top': tops, 'left': lefts});
		}
		resizeStatusLoginBox = true;
	}
}
function resizeLoginBox()
{
	if($("#loginbox") )
	{
		var tops = ($(window).height() - $("#loginbox").height()) / 2;
		var lefts = ($(window).width() - $("#loginbox").width()) / 2;
		if(resizeStatusLoginBox)
		{
			$("#loginbox").stop(true, true);
			$("#loginbox").animate({'top': tops, 'left': lefts}, 250, function() { $(this).css({'top': tops, 'left': lefts}); } );
		}
		else
		{
			$("#loginbox").css({'top': tops, 'left': lefts});
		}
		resizeStatusLoginBox = true;
	}
}
function resizeProjectList()
{
	if($("#project-list") )
	{
		var windowWidth = $(window).width() - 180;
		var projectWidth = $("#project-list > .list").children().length * 135;
		var listCount = parseInt(projectWidth / windowWidth) + 1;
		var windowWidthCount = parseInt(windowWidth / 135);

		var toWidth = projectWidth,
			toHeight = 135;
		if(listCount > 1)
		{
			toWidth = windowWidthCount * 135;
			toHeight = listCount * 135;
		}

		var tops = ($(window).height() - toHeight) / 2;
		var lefts = ($(window).width() - toWidth) / 2;
		$("#project-list > .list").css({
			width: windowWidthCount * 135,
			height: listCount * 135
		});

		if(resizeStatusProjectList)
		{
			$("#project-list > .list").stop(true, true);
			$("#project-list > .list").animate({'width': toWidth, 'height': toHeight, 'top': tops, 'left': lefts}, 250, function() { $(this).css({'width': toWidth, 'height': toHeight, 'top': tops, 'left': lefts}); } );
		}
		else
		{
			$("#project-list > .list").css({'width': toWidth, 'height': toHeight, 'top': tops, 'left': lefts});
		}
		resizeStatusProjectList = true;
	}
}
function showPopupSymbolUpload()
{
	var oriW = $("#popup-uploadsymbol > .body").width();
	var oriH = $("#popup-uploadsymbol > .body").height();

	$("#popup-uploadsymbol > .body > input").each(function(){ $(this)[0].value = ""; });

	$("body").css("overflow", "hidden");
	$("#popup-uploadsymbol").css("display", "block");

	$("#popup-container").stop(true, true);
	$("#popup-container").css({"display": "block", "opacity": 0.0});
	$("#popup-container").animate({
		opacity: 1.0,
	}, 250, function(){
		$(this).css({"opacity": 1.0});
		resizePopupSymbolUpload();
		tableResizing();
	});
}
function showPopupMemberjoin()
{
	var oriW = $("#popup-memberjoin > .body").width();
	var oriH = $("#popup-memberjoin > .body").height();

	$("#popup-memberjoin > .body > input").each(function(){ $(this)[0].value = ""; });

	$("body").css("overflow", "hidden");
	$("#popup-memberjoin").css("display", "block");

	$("#popup-container").stop(true, true);
	$("#popup-container").css({"display": "block", "opacity": 0.0});
	$("#popup-container").animate({
		opacity: 1.0,
	}, 250, function(){
		$(this).css({"opacity": 1.0});
	});
}
function hidePopupSymbolUpload()
{
	$("#popup-container").stop(true, true);
	$("#popup-container").animate({
		opacity: 0.0,
	}, 250, function(){
		$(this).css({"display": "none"});
		$("body").css("overflow", "");
		$("#popup-uploadsymbol").css("display", "none");
	});
}
function hidePopupMemberjoin()
{
	$("#popup-container").stop(true, true);
	$("#popup-container").animate({
		opacity: 0.0,
	}, 250, function(){
		$(this).css({"display": "none"});
		$("body").css("overflow", "");
		$("#popup-memberjoin").css("display", "none");
	});
}
function showPopupModifyProject()
{
	var oriW = $("#popup-modifyproject > .body").width();
	var oriH = $("#popup-modifyproject > .body").height();

	$("body").css("overflow", "hidden");
	$("#popup-modifyproject").css("display", "block");

	$("#popup-container").stop(true, true);
	$("#popup-container").css({"display": "block", "opacity": 0.0});
	$("#popup-container").animate({
		opacity: 1.0,
	}, 250, function(){
		$(this).css({"opacity": 1.0});
		tableResizing();
	});
}
function showPopupCreateProject()
{
	var oriW = $("#popup-createproject > .body").width();
	var oriH = $("#popup-createproject > .body").height();

	$("#popup-createproject > .body input").eq(0)[0].value = "";
	$("#popup-createproject > .body input").eq(1)[0].value = "1";
	$("#popup-createproject > .body input").eq(2)[0].value = "1";
	$("#popup-createproject > .body input").eq(3)[0].value = "1";

	$("body").css("overflow", "hidden");
	$("#popup-createproject").css("display", "block");

	$("#popup-container").stop(true, true);
	$("#popup-container").css({"display": "block", "opacity": 0.0});
	$("#popup-container").animate({
		opacity: 1.0,
	}, 250, function(){
		$(this).css({"opacity": 1.0});
	});
}
function hidePopupModifyProject()
{
	$("#popup-container").stop(true, true);
	$("#popup-container").animate({
		opacity: 0.0,
	}, 250, function(){
		$(this).css({"display": "none"});
		$("body").css("overflow", "");
		$("#popup-modifyproject").css("display", "none");
	});
}
function hidePopupCreateProject()
{
	$("#popup-container").stop(true, true);
	$("#popup-container").animate({
		opacity: 0.0,
	}, 250, function(){
		$(this).css({"display": "none"});
		$("body").css("overflow", "");
		$("#popup-createproject").css("display", "none");
	});
}
function showPopupInformation(w, h, idinstance)
{
	var oriW = $("#popup-information > .body").width();
	var oriH = $("#popup-information > .body").height();
	if(w)
	{
		var tops = ($(window).height() - h) / 2;
		var lefts = ($(window).width() - w) / 2;
		$("#popup-information > .body").stop(true, true);
		$("#popup-information > .body").animate({
			"top": tops,
			"left": lefts,
			"width": w,
			"height": h
		}, 250, function(){
			$(this).css({"top": tops, "left": lefts, "width": w, "height": h});
		});
	}
	$("body").css("overflow", "hidden");
	$("#popup-information").css("display", "block");

	$("#popup-container").stop(true, true);
	$("#popup-container").css({"display": "block", "opacity": 0.0});
	$("#popup-container").animate({
		opacity: 1.0,
	}, 250, function(){
		$(this).css({"opacity": 1.0});
	});
	
	//여기서 팝업창 띄울 놈 얻어옴
	getinstancedata(idinstance)
    	geteventpath(idinstance)
    	getlog(idinstance)

}
function showPopupEventpath(w, h)
{
	var oriW = $("#popup-eventpath > .body").width();
	var oriH = $("#popup-eventpath > .body").height();
	if(w)
	{
		var tops = ($(window).height() - h) / 2;
		var lefts = ($(window).width() - w) / 2;
		$("#popup-eventpath > .body").stop(true, true);
		$("#popup-eventpath > .body").animate({
			"top": tops,
			"left": lefts,
			"width": w,
			"height": h
		}, 250, function(){
			$(this).css({"top": tops, "left": lefts, "width": w, "height": h});
		});
	}
	$("body").css("overflow", "hidden");
	$("#popup-eventpath").css("display", "block");

	$("#popup-container").stop(true, true);
	$("#popup-container").css({"display": "block", "opacity": 0.0});
	$("#popup-container").animate({
		opacity: 1.0,
	}, 250, function(){
		$(this).css({"opacity": 1.0});
	});
}
function showPopupLogdata(w, h)
{
	var oriW = $("#popup-logdata > .body").width();
	var oriH = $("#popup-logdata > .body").height();
	if(w)
	{
		var tops = ($(window).height() - h) / 2;
		var lefts = ($(window).width() - w) / 2;
		$("#popup-logdata > .body").stop(true, true);
		$("#popup-logdata > .body").animate({
			"top": tops,
			"left": lefts,
			"width": w,
			"height": h
		}, 250, function(){
			$(this).css({"top": tops, "left": lefts, "width": w, "height": h});
		});
	}
	$("body").css("overflow", "hidden");
	$("#popup-logdata").css("display", "block");

	$("#popup-container").stop(true, true);
	$("#popup-container").css({"display": "block", "opacity": 0.0});
	$("#popup-container").animate({
		opacity: 1.0,
	}, 250, function(){
		$(this).css({"opacity": 1.0});
	});
}
function showConfirm()
{
	resizeConfirm();

	var oriW = $("#warning-alert > .body").width();
	var oriH = $("#warning-alert > .body").height();
	
	$("body").css("overflow", "hidden");

	$("#warning-alert").stop(true, true);
	$("#warning-alert").css({"display": "block", "opacity": 0.0});
	$("#warning-alert").animate({
		opacity: 1.0,
	}, 250, function(){
		$(this).css({"opacity": 1.0});
	});
}

function hidePopupInformation()
{
	$("#popup-container").stop(true, true);
	$("#popup-container").animate({
		opacity: 0.0,
	}, 250, function(){
		$(this).css({"display": "none"});
		$("body").css("overflow", "");
		$("#popup-information").css("display", "none");
	});
}
function hidePopupEventpath()
{
	$("#popup-container").stop(true, true);
	$("#popup-container").animate({
		opacity: 0.0,
	}, 250, function(){
		$(this).css({"display": "none"});
		$("body").css("overflow", "");
		$("#popup-eventpath").css("display", "none");
	});
}
function hidePopupLogdata()
{
	$("#popup-container").stop(true, true);
	$("#popup-container").animate({
		opacity: 0.0,
	}, 250, function(){
		$(this).css({"display": "none"});
		$("body").css("overflow", "");
		$("#popup-logdata").css("display", "none");
	});
}
function hideConfirm()
{
	$("#popup-container").stop(true, true);
	$("#popup-container").animate({
		opacity: 0.0,
	}, 250, function(){
		$(this).css({"display": "none"});
		$("body").css("overflow", "");
		$("#warning-alert").css("display", "none");
	});
}

$(document).ready(function()
{
	$("#container").addClass("container-js");
	if(supportsSVG()) $("#container").addClass("svg");
	if(navigator.userAgent.match(/applewebkit/i))
	{
		if(!navigator.geolocation)
		{
			$("#container").addClass("decelerate");
		}
		else
		{
			if (navigator.platform.match(/ipad/i) ||
				navigator.platform.match(/iphone/i) ||
				navigator.platform.match(/ipod/i) ) $("#container").addClass("ios");
		}
		if (navigator.userAgent.match(/chrome/i) &&
			navigator.userAgent.match(/windows/i) ) $("#container").addClass("noinset");
	}

	var profileCount = 0;
	var timer = null;
	profileShow = function(obj) {
		if(profileCount == 0)
		{
			clearTimeout(timer);
			$("#profile-menu").stop(true, true);
			$("#profile-menu").css({"display": "block", "opacity": 1.0});
			$("#header > .navbar-profile > .profile > img").css("opacity", 0.16);
		}
		profileCount ++;
	};
	profileHide = function() {
		profileCount --;
		if(profileCount == 0)
		{
			$("#profile-menu").stop(true, true);
			$("#profile-menu").css("opacity", 0.0);
			$("#header > .navbar-profile > .profile > img").css("opacity", 1.0);
			timer = setTimeout("$(\"#profile-menu\").css(\"display\", \"none\");", 100);
		}
	};
	$("#header > .navbar-profile > .profile > img").hover(profileShow, profileHide);
	$("#profile-menu").hover(profileShow, profileHide);
});


// Stylesheet is load-complate
$("head").styleReady(function(){
	$("body").css("display", "block");
	
	if($("html").hasClass("project-select") )
	{
		copyToClipboard("#project-list > .list > div > label > span", copyThis);
	}

	// Graph rendering
	if($("body").hasClass("insight") )
	{
		$("#dailyES").ready(function(){
			Raphael.custom.areaGraph("dailyes", "#dailyES", {"lineWidth": 1, "horizonLine": false, "verticalLine": false, "leftgutter": 0, "topgutter": 5,
				"color": "#dca763", "lineColor": "#3a3f42", "textColor": "#303335", "autoResize": true });
		});
		$("#typeES").ready(function(){
             $.ajax({
                type: 'get'
              , url: 'typees/color'
              , success : function(data) {
                        var info = {"lineWidth": 1, "horizonLine": false, "verticalLine": false, "leftgutter": 0, "topgutter": 5,
        				"lineColor": "#ffffff", "textColor": "#303335", "labelPos": "east", "colorTable": [], "autoResize": true }
                        info['colorTable'] = data
                        Raphael.custom.pieGraph("typees", "#typeES", info);
                   }
               })
		});
	}
	if($("body").hasClass("error") )
	{
        	$("#event-path-parent").ready(function(){
			//Raphael.custom.eventPath("./data3", "#event-path", {"height": 230, "contentWidth": 20, "contentHeight": 20, "textColor": "#303335", "colorTable": [ "#de6363", "#5a9ccc", "#72c380", "#cccdc7", "#9d61dd", "#6371dc", "#dca763", "#a96f6e", "#6fa79a", "#737270" ], "autoResize": true, "topgutter": 5, "bottomgutter": -10 })
            $.ajax({
                type: 'get'
              , url: 'eventpath'
              , success : function(data) {
                        sankeyloading = true
                        sankeydata = data
                        sankeydraw(data)
                   }
               })
		});
    }

  	if($("body").hasClass("statistics") )
	{
		/*$("#cecs").ready(function(){
			Raphael.custom.pieGraph("./data2", "#cecs", {"lineWidth": 1, "horizonLine": false, "verticalLine": false, "leftgutter": 0, "topgutter": 5,
				"lineColor": "#ffffff", "textColor": "#303335", "labelPos": "east", "colorTable": [ "#de6363", "#5a9ccc", "#72c380", "#cccdc7", "#9d61dd", "#6371dc", "#dca763", "#a96f6e", "#6fa79a", "#737270" ], "autoResize": true });
		});
       $("#cecs").highcharts({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: 'Class Error Rate'
            },
            colors: [ "#de6363", "#5a9ccc", "#72c380", "#cccdc7", "#9d61dd", "#6371dc", "#dca763", "#a96f6e", "#6fa79a", "#737270" ],
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        color: '#000000',
                        connectorColor: '#000000',
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                    }
                }
            },
            series: [{
                type: 'pie',
                name: 'Browser share',
                data: [
                    ['Firefox',   45.0],
                    ['IE',       26.8],
                    {
                        name: 'Chrome',
                        y: 12.8,
                        sliced: true,
                        selected: true
                    },
                    ['Safari',    8.5],
                    ['Opera',     6.2],
                    ['Others',   0.7]
                ]
            }]
        });

		function exampleData() {
			return  [ 
				{
					key: "Cumulative Return",
					values: [
						{ 
							"label" : "CDS / Options" ,
							"value" : -29.765957771107
						} , 
						{ 
							"label" : "Cash" , 
							"value" : 0
						} , 
						{ 
							"label" : "Corporate Bonds" , 
							"value" : 32.807804682612
						} , 
						{ 
							"label" : "Equity" , 
							"value" : 196.45946739256
						} , 
						{ 
							"label" : "Index Futures" ,
							"value" : 0.19434030906893
						} , 
						{ 
							"label" : "Options" , 
							"value" : -98.079782601442
						} , 
						{ 
							"label" : "Preferred" , 
							"value" : -13.925743130903
						} , 
						{ 
							"label" : "Not Available" , 
							"value" : -5.1387322875705
						}
					]
				}
			];
		}	

		nv.addGraph(function() {
			var chart = nv.models.discreteBarChart()
				.x(function(d) { return d.label })
				.y(function(d) { return d.value })
				.color([ "#de6363", "#5a9ccc", "#72c380", "#cccdc7", "#9d61dd", "#6371dc", "#dca763", "#a96f6e", "#6fa79a", "#737270" ])
				.staggerLabels(true)
				.tooltips(false)
				.showValues(true);

			d3.select('#decs svg')
				.datum(exampleData())
				.transition().duration(500)
				.call(chart);

			nv.utils.windowResize(chart.update);

			return chart;
		});

		nv.addGraph(function() {
			var chart = nv.models.discreteBarChart()
				.x(function(d) { return d.label })
				.y(function(d) { return d.value })
				.color([ "#de6363", "#5a9ccc", "#72c380", "#cccdc7", "#9d61dd", "#6371dc", "#dca763", "#a96f6e", "#6fa79a", "#737270" ])
				.staggerLabels(true)
				.tooltips(false)
				.showValues(true);

			d3.select('#ebas svg')
				.datum(exampleData())
				.transition().duration(500)
				.call(chart);

			nv.utils.windowResize(chart.update);

			return chart;
		});
		$(function () {
			$('#vers').highcharts({
				chart: {
					type: 'column'
				},
				title: {
					text: 'Version Error Rate'
				},
				colors: [ "#de6363", "#5a9ccc", "#72c380", "#cccdc7", "#9d61dd", "#6371dc", "#dca763", "#a96f6e", "#6fa79a", "#737270" ],
				xAxis: {
					categories: ['Apples', 'Oranges', 'Pears', 'Grapes', 'Bananas']
				},
				yAxis: {
					min: 0,
					title: {
						text: 'Version Error Rate'
					},
					stackLabels: {
						enabled: true,
						style: {
							fontWeight: 'bold',
							color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
						}
					}
				},
				legend: {
					align: 'right',
					x: -70,
					verticalAlign: 'top',
					y: 20,
					floating: true,
					backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColorSolid) || 'white',
					borderColor: '#CCC',
					borderWidth: 1,
					shadow: false
				},
				tooltip: {
					formatter: function() {
						return '<b>'+ this.x +'</b><br/>'+
							this.series.name +': '+ this.y +'<br/>'+
							'Total: '+ this.point.stackTotal;
					}
				},
				plotOptions: {
					column: {
						stacking: 'normal',
						dataLabels: {
							enabled: true,
							color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
						}
					}
				},
				series: [{
					name: 'John',
					data: [5, 3, 4, 7, 2]
				}, {
					name: 'Jane',
					data: [2, 2, 3, 2, 1]
				}, {
					name: 'Joe',
					data: [3, 4, 4, 2, 5]
				}]
			});
		});
		*/
	}

	/** Component Start **/
	// Dropdown(multiple select) component
	$(".dropdown.multiple").ready(function(){
		$(".dropdown.multiple").each(function(){
			var me = $(this);
			var chd = me.children("a");
			var name = chd.html();
			var codename = me.children("input").attr("name");

			chd.html("<div></div>");
			chd = chd.children("div");
			chd.addClass("checkbox").addClass("half");
			chd.html("<span></span><label>" + name + "</label>");

			chd = me.children("span");

			me.children("div").children("ul").children("li").each(function(){
				var chd2;
				var name2 = $(this).children("a").html();

				$(this).html("<div></div>");
				chd2 = $(this).children("div");
				chd2.addClass("checkbox");
				chd2.html("<span></span><label>" + name2 + "</label><input type=\"hidden\" name=\"" + codename + "[]\" data-group=\"" + name + "\" data-value=\"" + name2 + "\" />");
			});
			me.children("input").remove();
		});
	});

	// Radiobox component
	$(".radiobox").ready(function()
	{
		// Initialize
		var radiobox_objects = $(".radiobox");
		for(var i = 0; i < radiobox_objects.length; i ++)
		{
			var me = radiobox_objects.eq(i);
			me.attr("data-name", me.children("input").attr("name") );
			me.attr("data-value", me.children("input").attr("value") );

			var group_info = $(".radiobox[data-name=" + me.attr("data-name") + "]");
			if(group_info.length > 1) me.children("input").remove();

			if($(this).children("span").attr("data-value") == "checked")
				group_info.eq(0).children("input").attr("value", me.attr("data-value") );
		}

		// Click event
		$(".radiobox").click(function(){
			var group_info = $(".radiobox[data-name=" + $(this).attr("data-name") + "]");
			group_info.children("span[data-value=checked]").attr("data-value", "");
			group_info.eq(0).children("input").attr("value", $(this).attr("data-value") );
			$(this).children("span").attr("data-value", "checked");
		});
	});

	// Checkbox component
	$(".checkbox").ready(function()
	{
		// Initialize
		$(".checkbox").each(function(index){
			if($(this).children("input").attr("value") )
				$(this).attr("data-value", "checked");
		});

		// Click event
		$(".checkbox").click(function() {
			if($(this).attr("data-value") == "checked" || $(this).attr("data-value") == "halfed")
			{
				$(this).attr("data-value", "");
				$(this).children("input").removeAttr("value");
			}
			else
			{
				$(this).attr("data-value", "checked");
				$(this).children("input").attr("value", $(this).children("input").attr("data-value"));
			}
			if($(this).parent().parent().hasClass("dropdown") )
			{
				if($(this).attr("data-value") == "checked")
				{
					$(this).parent().parent().children("div").children("ul").children("li").children(".checkbox[data-value!=checked]").click();
				}
				else
				{
					$(this).parent().parent().children("div").children("ul").children("li").children(".checkbox[data-value=checked]").click();
				}
			}
			else if($(this).parent().parent().parent().parent().hasClass("dropdown") )
			{
				var cnt1 = $(this).parent().parent().children("li").children(".checkbox[data-value=checked]").length;
				var cnt2 = $(this).parent().parent().children("li").length;

				if(cnt1 == 0)				
					$(this).parent().parent().parent().parent().children("a").children(".checkbox").attr("data-value", "");
				else if(cnt1 == cnt2)
					$(this).parent().parent().parent().parent().children("a").children(".checkbox").attr("data-value", "checked");
				else
					$(this).parent().parent().parent().parent().children("a").children(".checkbox").attr("data-value", "halfed");
			}
		});
	});

	// Dropdown component
	$(".dropdown").ready(function()
	{
		itemClickEvent = function(obj) {
			$(this).parent().children("li[data-value=\"true\"]").attr("data-value", "false");
			if($(this).attr("data-value") == "true")
				$(this).attr("data-value", "false");
			else
				$(this).attr("data-value", "true");
			$(this).parent().parent().parent().children("a").html($(this).children("a").html());
			$(this).parent().parent().parent().children("input").attr("value", $(this).index() + 1);

            $(this).parent().parent().hide();
        }

        // Dialog showing
        showDialog = function(th)
        {
            var h = oriH = $(th).offset().top + $(th).outerHeight() - $(window).scrollTop();
            for(var i = 0; i < $(th).children("div").children("ul").children().length; i ++)
            {
                if($(th).children("div").children("ul").children().eq(i).css("display") == "none") continue;
                if(h + 36 > window.innerHeight) break;
                h += 36;
            }
            $(th).children("div").width("");
            $(th).children("div").show();
            $(th).children("div").width($(th).children("div").width() );
            $(th).children("div").height(h - oriH);
        }

        // Initialize
        $(".dropdown").each(function(index){
            $(this).children("div").children("ul").children("li").attr("data-value", "false");
            $(this).children("div").children("ul").children("li").eq($(this).children("input").attr("value") - 1).attr("data-value", "true");
            $(this).children("a").html($(this).children("div").children("ul").children("li").eq($(this).children("input").attr("value") - 1).children("a").html());

            $(this).children("div").css("min-width", $(this).width() + 42);
        });

        // Mouse over/out event
        $(".dropdown").hover(function() {
            $(this).attr("data-type", "over");
            if($(this).hasClass("simple") )
                showDialog(this);
        }, function() {
            $(this).attr("data-type", "");
            $(this).children("div").hide();
        });

        // Click event
        $(".dropdown").click(function() {
            if(!$(this).hasClass("simple") )
            {
                if($(this).attr("data-type") != "clicked"){
                    $(this).attr("data-type", "clicked");
                    showDialog(this);
                }
                else
                {
                    $(this).attr("data-type", "");
                    $(this).children("div").hide();
                }
            }
        });
        // Click to Dropdown component's item event
        $(".dropdown:not(.multiple)").each(function(){
            $(this).children("div").children("ul").children("li").click(itemClickEvent);
        });

        // Tags-list component
        $(".tags-list").ready(function()
        {
            // Add to hidden input
            addHiddenInput = function(obj, name) {
                if(obj.children("input") != null)
                    obj.append("<input type=\"hidden\" name=\"" + name + "[]\" value=\"" + obj.html() + "\" />");
            }

            // Add event
            addEvent = function(obj) {
                if($(this).css("display") != "none")
                {
                    var newME = $(this).parent().parent().parent().parent().children("li:nth-last-child(1)").before("<li></li>").parent().children("li:nth-last-child(2)");
                    newME.click(restoreEvent);
                    addHiddenInput(newME, $(this).parent().parent().attr("data-name") );
                    newME.html($(this).parent().parent().parent().children("a").html());
                    newME.append("<i></i>");

                    $(this).parent().parent().parent().children("a").html("Add More")
                        $(this).css("display", "none");
                }
            }
                // Restore event
            restoreEvent = function(obj) {
                var dropdown = $(this).parent().children("li:nth-last-child(1)").children("div").children("ul");
                dropdown.append("<li data-value=\"false\"><a>" + $(this).html() + "</a></li>");
                dropdown.children("li:nth-last-child(1)").click(itemClickEvent).click(addEvent);
                $(this).remove();
                var csrftoken = getCookie('csrftoken')
                var deletetag = {'tag' : $(this).text()}
                $.ajax({
                      type: 'post'
                    , url: 'tag/delete'
                    , data: deletetag
                    , beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                            // Send the token to same-origin, relative URLs only.
                            // Send the token only if the method warrants CSRF protection
                            // Using the CSRFToken value acquired earlier
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                })
            }
            // Initialize
            $(".tags-list").each(function(index){
                var child = $(this).children("ul").children("li");
                $(this).attr("data-name", $(this).children("input[type=hidden]").attr("name") );
                $(this).children("input[type=hidden]").remove();
                for(var i = 0; i < child.length; i ++)
                {
                    if(!child.eq(i).hasClass("dropdown") )
                    {
                        addHiddenInput(child.eq(i), $(this).attr("data-name") );
                        child.eq(i).click(restoreEvent);
                    }
                }

                if($(this).hasClass("user-input") )
                {
                    $(this).children("ul").children(".dropdown").off("click mouseenter mouseleave").click(function(){
                        $(this).attr("data-type", "clicked");
                        $(this).children("input").focus();
                    });
                    $(this).children("ul").children(".dropdown").children("input").keyup(function(event){
                        if(event.keyCode == 13)
                        {
                            var sendtag = {'tag' : $(this)[0].value }
                            var csrftoken = getCookie('csrftoken')
                             $.ajax({
                              type: 'post'
                            , url: 'tag/new'
                            , data:  sendtag
                            , beforeSend: function(xhr, settings) {
                                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                                    // Send the token to same-origin, relative URLs only.
                                    // Send the token only if the method warrants CSRF protection
                                    // Using the CSRFToken value acquired earlier
                                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                }
                            }
                            ,success: function(data){

                                 var newME = $('#newtag').children("li:nth-last-child(1)").before("<li></li>").parent().children("li:nth-last-child(2)");
                                newME.click(restoreEvent);
                                newME.html($('#inputtag').parent().children('input')[0].value);
                                newME.append("<i></i>");
                                $('inputtag').parent().children('input')[0].value = "";
                                $('#inputtag').attr("data-type", "");
                            }
                         })

                        }
                        else if(event.keyCode == 27)
                        {
                            $(this).parent().attr("data-type", "");
                        }
                    });
                }
                else
                {
                    $(".tags-list .dropdown > div").css("min-width", parseInt($(".tags-list .dropdown > div").css("min-width") ) - 26);
                    $(".tags-list .dropdown > div li").click(addEvent);
                }
            });
		});
	});

	// Scrollbar component
	$(".scrollbar").ready(function()
	{
		// Initialize
		$(".scrollbar").each(function(index){
			var index = $(this).children("input").attr("value");
			var persent = 100.0 / ($(this).children("ul").children("li").length - 1);
			$(this).children("ul").children("li").each(function(){
				if($(this).children("a")[0].innerText == index)
					$(this).attr("data-value", "true");
				$(this).css("width", persent+"%");
			});
		});

		// Mouse over/out event
		$(".scrollbar > ul > li").hover(function() {
			if($(this).attr("data-value") )
				$(this).attr("data-temp", $(this).attr("data-value"));
			else
				$(this).attr("data-temp", "false");
			$(this).attr("data-value", "true");
		}, function() {
			$(this).attr("data-value", $(this).attr("data-temp"));
			$(this).removeAttr("data-temp");
		});
		$(".scrollbar > ul > li").click(function(){
			$(this).parent().children("li[data-value=true]").attr("data-value", "false");
			$(this).attr({"data-value":"true", "data-temp":"true"});
			$(this).parent().parent().children("input").attr("value", $(this).children("a")[0].innerText);
		});
	});

	$(".button").click(function(){
		if(!$(this).hasClass("event") )
		{
			var parent = $(this).parent();
			while(parent.get(0) != null)
			{
				if(parent.get(0).tagName == "FORM")
					parent.submit();
				parent = parent.parent();
			}
		}
		else
		{
			eval($(this).attr("data-event") );
		}
	});

	$(".checkbox.red").click(function() {
		if($(this).attr("data-value") == "checked"){
			$(".checkbox:not(.red)[data-value=checked] > input[name=\""+$(this).children("input").attr("name")+"\"]").each(function() { $(this).parent().click(); });
		}
	});
	$(".checkbox:not(.red)").click(function() {
		if($(this).attr("data-value") == "checked"){
			$(".checkbox.red[data-value=checked] > input[name=\""+$(this).children("input").attr("name")+"\"]").each(function() { $(this).parent().click(); });
		}
	});
	$("table.sort > thead > tr > td").click(function(){
		if($(this).hasClass("asc") )
		{
			$(this).parent().children().removeClass("asc desc");
			$(this).removeClass("asc").addClass("desc");
		}
		else
		{
			$(this).parent().children().removeClass("asc desc");
			$(this).removeClass("desc").addClass("asc");
		}
	});

	/** Component End **/

	$("#symbolUploading").hide();
	$("#symbolUpload").submit(function(event){
		$("#symbolUpload").hide();
		$("#symbolUploading").show();
	});
	$("#uploadTrg").load(function(){
		alert("The symbol-file is uploaded!");
		$("#symbolUpload").show();
		$("#symbolUploading").hide();
	});

	popup_hide = function() {
		$("#popup-info").stop(true, true);
		$("#popup-info").animate({
			opacity: 0.0
		}, 250, function(){
			$(this).css("display", "none");
		});
	};
	popup_show = function(obj) {
		$("#popup-info").stop(true, true);
		$("#popup-info").css({"display": "block"});
		$("#popup-info").animate({ opacity: 0.9 }, 250, function() {} );
		if(obj)
		{
			$("#popup-info").css("top", obj.position().top + 20);
			$("#popup-info").css("left", obj.position().left - 116);
		}
	};

	if($("#popup-title") )
	{
		$("#popup-info").hover(function(){popup_show();}, popup_hide);
		$("table.content-large tbody .float > span.red").hover(function() {
			$("#popup-title").html("Critical");
			popup_show($(this));
		},popup_hide);

		$("table.content-large tbody .float > span.blue").hover(function() {
			$("#popup-title").html("Major");
			popup_show($(this));
		},popup_hide);

		$("table.content-large tbody .float > span.green").hover(function() {
			$("#popup-title").html("Minor");
			popup_show($(this));
		},popup_hide);

		$("table.content-large tbody .float > span.gray").hover(function() {
			$("#popup-title").html("Unhandler");
			popup_show($(this));
		},popup_hide);
	}
	if($("#critical-information") )
	{
		$("#critical-information .infobox > .createdate").hover(function() {
			$("#popup-title").html("Create Date");
			popup_show($(this));
		},popup_hide);

		$("#critical-information .infobox > .updatedate").hover(function() {
			$("#popup-title").html("Update Date");
			popup_show($(this));
		},popup_hide);

		$("#critical-information .infobox > .occur").hover(function() {
			$("#popup-title").html("Occur Count");
			popup_show($(this));
		},popup_hide);

		$("#critical-information .infobox > .reappear").hover(function() {
			$("#popup-title").html("Error re-appear");
			popup_show($(this));
		},popup_hide);

		$("#critical-information .infobox > .status").hover(function() {
			$("#popup-title").html("Status");
			popup_show($(this));
		},popup_hide);

		$("#critical-information .infobox > .wifi").hover(function() {
			$("#popup-title").html("Wifi");
			popup_show($(this));
		},popup_hide);

		$("#critical-information .infobox > .gps").hover(function() {
			$("#popup-title").html("GPS");
			popup_show($(this));
		},popup_hide);

		$("#critical-information .infobox > .mobilenetwork").hover(function() {
			$("#popup-title").html("Mobile Network");
			popup_show($(this));
		},popup_hide);

		$("#critical-information .infobox > .memory").hover(function() {
			$("#popup-title").html("Memory");
			popup_show($(this));
		},popup_hide);
	}

	// Auto-resize table
	addWindowResize(tableResizing)();

	// Auto-resize popup-information
	//$("#popup-information").click(hidePopupInformation);
	var bodyChecker_info = false,
		bodyChecker_evpt = false,
		bodyChecker_logd = false,
		bodyChecker_join = false,
		bodyChecker_addP = false,
		bodyChecker_noti = false,
		bodyChecker_upsy = false.
		bodyChecker_confirm = false;
	$("#popup-uploadsymbol").click(function(){ if(bodyChecker_upsy == false){ hidePopupSymbolUpload(); } bodyChecker_upsy = false; });
	$("#popup-memberjoin").click(function(){ if(bodyChecker_join == false){ hidePopupMemberjoin(); } bodyChecker_join = false; });
	$("#popup-information").click(function(){ if(bodyChecker_info == false){ hidePopupInformation(); } bodyChecker_info = false; });
	$("#popup-eventpath").click(function(){ if(bodyChecker_evpt == false){ hidePopupEventpath(); } bodyChecker_evpt = false; });
	$("#popup-logdata").click(function(){ if(bodyChecker_logd == false){ hidePopupLogdata(); } bodyChecker_logd = false; });
	$("#popup-modifyproject").click(function(){ if(bodyChecker_addP == false){ hidePopupModifyProject(); } bodyChecker_addP = false; });
	$("#popup-createproject").click(function(){ if(bodyChecker_addP == false){ hidePopupCreateProject(); } bodyChecker_addP = false; });
	$("#warning-alert").click(function(){ if(bodyChecker_confirm == false){ hideConfirm(); } bodyChecker_confirm = false; });
	$("#popup-uploadsymbol > .body").click(function(){ bodyChecker_upsy = true; });
	$("#popup-memberjoin > .body").click(function(){ bodyChecker_join = true; });
	$("#popup-information > .body").click(function(){ bodyChecker_info = true; });
	$("#popup-modifyproject > .body").click(function(){ bodyChecker_addP = true; });
	$("#popup-createproject > .body").click(function(){ bodyChecker_addP = true; });
	$("#warning-alert > .body").click(function(){ bodyChecker_confirm = true; });

	$("#popup-notification div").click(function(){
		if(bodyChecker_noti == false)
		{
			document.location = $(this).attr("data-href");
		}
		else
		{
			$(this).children("span").hide();
			$(this).animate({
				height: 0,
				"padding-top": 0,
				"padding-bottom": 0
			}, 250, function(){
				$(this).hide();
				$(this).addClass("read");
				$("#profile-menu > div:nth-last-child(1) > div > span:nth-child(2) > .notification").attr("data", $("#popup-notification > div:not(.read)").length);
				if($("#popup-notification > div:visible").length == 0)
					$("#popup-notification").hide();
			})
		}
		bodyChecker_noti = false;
	});
	$("#popup-notification span").click(function(){ bodyChecker_noti = true; });

	if($("#popup-notification > div:not(.read)").length != 0)
	{
		$("#profile-menu > div:nth-last-child(1) > div > span:nth-child(2) > .notification").attr("data", $("#popup-notification > div:not(.read)").length);
		$("#poup-information > div:not(.read)").show();
		$("#popup-notification").show();
	}

	addWindowResize(resizePopupSymbolUpload)();
	addWindowResize(resizePopupMemberjoin)();
	addWindowResize(resizePopupNotification)();
	addWindowResize(resizePopupInformation)();
	addWindowResize(resizePopupEventpath)();
	addWindowResize(resizePopupLogdata)();
	addWindowResize(resizeModifyProject)();
	addWindowResize(resizeCreateProject)();
	addWindowResize(resizeLoginBox)();
	addWindowResize(resizeProjectList)();
	addWindowResize(resizeConfirm)();
});

function adjustErrorListStyle(){
    itemClickEvent1 = function(obj) {
        $(this).parent().children("li[data-value=\"true\"]").attr("data-value", "false");
        if($(this).attr("data-value") == "true")
            $(this).attr("data-value", "false");
        else
            $(this).attr("data-value", "true");
        $(this).parent().parent().parent().children("a").html($(this).children("a").html());
        $(this).parent().parent().parent().children("input").attr("value", $(this).index() + 1);

        $(this).parent().parent().hide();

        var iderror = $(this).parents().eq(4).attr('iderror')
        var csrftoken = getCookie('csrftoken')
        var status = $(this).index()
        $.ajax({
              type: 'post'
            , url: '/urqa/project/'+ project_id +'/errors/' + iderror + '/status'
            , data: {'status' : status}
            , beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        })
    }

    // Dialog showing
    showDialog1 = function(th)
    {
        var h = oriH = $(th).offset().top + $(th).outerHeight() - $(window).scrollTop();
        for(var i = 0; i < $(th).children("div").children("ul").children().length; i ++)
        {
            if($(th).children("div").children("ul").children().eq(i).css("display") == "none") continue;
            if(h + 36 > window.innerHeight) break;
            h += 36;
        }
        $(th).children("div").width("");
        $(th).children("div").show();
        $(th).children("div").width($(th).children("div").width() );
        $(th).children("div").height(h - oriH);
    }

    // Initialize
    $(".updated-dropdown").each(function(index){
        if($(this).parent().parent().hasClass('updated-tags'))  return;
        $(this).children("div").children("ul").children("li").attr("data-value", "false");
        $(this).children("div").children("ul").children("li").eq($(this).children("input").attr("value")).attr("data-value", "true");
        $(this).children("a").html($(this).children("div").children("ul").children("li").eq($(this).children("input").attr("value")).children("a").html());

        $(this).children("div").css("min-width", $(this).width() + 42);
    });

    // Mouse over/out event
    $(".updated-dropdown").hover(function() {
        $(this).attr("data-type", "over");
        if($(this).hasClass("simple") )
            showDialog1(this);
    }, function() {
        $(this).attr("data-type", "");
        $(this).children("div").hide();
    });

    // Click event
    $(".updated-dropdown").click(function() {
        if(!$(this).hasClass("simple") )
        {
            if($(this).attr("data-type") != "clicked"){
                $(this).attr("data-type", "clicked");
                showDialog1(this);
            }
            else
            {
                $(this).attr("data-type", "");
                $(this).children("div").hide();
            }
        }
    });
    // Click to Dropdown component's item event
    $(".updated-dropdown:not(.multiple)").each(function(){
        $(this).children("div").children("ul").children("li").click(itemClickEvent1);
    });








    //Add event
    addEvent1 = function(obj) {
        if($(this).css("display") != "none")
        {
            var newME = $(this).parent().parent().parent().parent().children("li:nth-last-child(1)").before("<li></li>").parent().children("li:nth-last-child(2)");
            newME.click(restoreEvent1);
            addHiddenInput(newME, $(this).parent().parent().attr("data-name") );
            newME.html($(this).parent().parent().parent().children("a").html());
            newME.append("<i></i>");

            $(this).parent().parent().parent().children("a").html("Add Tag")
                $(this).css("display", "none");
        }
    }
        // Restore event
    restoreEvent1 = function(obj) {
        if($(this).parent().parent().hasClass("user-input") )
        {
            var tag = $(this).text();
            var dropdown = $(this).parent().children("li:nth-last-child(1)").children("div").children("ul");
            //dropdown.append("<li data-value=\"false\"><a>" + $(this).html() + "</a></li>");
            //dropdown.children("li:nth-last-child(1)").click(itemClickEvent1).click(addEvent1);
            var iderror = $(this).parents().eq(3).attr('iderror')
            $(this).remove();
            var csrftoken = getCookie('csrftoken')
            $.ajax({
                  type: 'post'
                , url: '/urqa/project/'+ project_id +'/errors/' + iderror + '/tag/delete'
                , data: {'tag' : tag}
                , beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                        // Send the token to same-origin, relative URLs only.
                        // Send the token only if the method warrants CSRF protection
                        // Using the CSRFToken value acquired earlier
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            })
        }
    }
    // Initialize
    $(".updated-tags").each(function(index){
        var child = $(this).children("ul").children("li");
        $(this).attr("data-name", $(this).children("input[type=hidden]").attr("name") );
        $(this).children("input[type=hidden]").remove();
        for(var i = 0; i < child.length; i ++)
        {
            if(!child.eq(i).hasClass("updated-dropdown") )
            {
                addHiddenInput(child.eq(i), $(this).attr("data-name") );
                child.eq(i).click(restoreEvent1);
            }
        }

        if($(this).hasClass("user-input") )
        {
            $(this).children("ul").children(".updated-dropdown").off("click mouseenter mouseleave").click(function(){
                $(this).attr("data-type", "clicked");
                $(this).children("input").focus();
            });
            $(this).children("ul").children(".updated-dropdown").children("input").keyup(function(event){
                if(event.keyCode == 13)
                {
                    if($(this)[0].value.length == 0)
                    {
                        $(this).parent().attr("data-type", "");
                        return;
                    }
                    var this_save = this;
                    var csrftoken = getCookie('csrftoken')
                    var iderror = $(this).parents().eq(4).attr('iderror')
                    $.ajax({
                      type: 'post'
                    , url: '/urqa/project/'+ project_id +'/errors/' + iderror + '/tag/new'
                    , beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                            // Send the token to same-origin, relative URLs only.
                            // Send the token only if the method warrants CSRF protection
                            // Using the CSRFToken value acquired earlier
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }}
                    , data: {'tag':$(this)[0].value}
                    , success : function(data) {
                            if(data == 'success')
                            {
                                var newME = $(this_save).parent().parent().children("li:nth-last-child(1)").before("<li></li>").parent().children("li:nth-last-child(2)");
                                newME.click(restoreEvent1);
                                newME.html($(this_save)[0].value);
                                newME.append("<i></i>");
                                $(this_save)[0].value = "";
                                $(this_save).parent().attr("data-type", "");
                            }
                            else
                                $(this_save).parent().attr("data-type", "");
                        }
                    })
                }
                else if(event.keyCode == 27)
                {
                    $(this).parent().attr("data-type", "");
                }
            });
        }
    });

    popup_hide = function() {
		$("#popup-info").stop(true, true);
		$("#popup-info").animate({
			opacity: 0.0
		}, 250, function(){
			$(this).css("display", "none");
		});
	};
	popup_show = function(obj) {
		$("#popup-info").stop(true, true);
		$("#popup-info").css({"display": "block"});
		$("#popup-info").animate({ opacity: 0.9 }, 250, function() {} );
		if(obj)
		{
			$("#popup-info").css("top", obj.position().top + 20);
			$("#popup-info").css("left", obj.position().left - 116);
		}
	};

	if($("#popup-title") )
	{
		$("#popup-info").hover(function(){popup_show();}, popup_hide);
		$("table.content-large tbody .float > span.red").hover(function() {
			$("#popup-title").html("Critical");
			popup_show($(this));
		},popup_hide);

		$("table.content-large tbody .float > span.blue").hover(function() {
			$("#popup-title").html("Major");
			popup_show($(this));
		},popup_hide);

		$("table.content-large tbody .float > span.green").hover(function() {
			$("#popup-title").html("Minor");
			popup_show($(this));
		},popup_hide);

		$("table.content-large tbody .float > span.gray").hover(function() {
			$("#popup-title").html("Unhandler");
			popup_show($(this));
		},popup_hide);
	}
}