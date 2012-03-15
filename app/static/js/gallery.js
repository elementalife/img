function format_size (size) {
	if (size >= 1073741824) {
		return (size / 1073741824).toFixed(2) + ' Gb';
	}
	if (size >= 1048576) {
		return (size / 1048576).toFixed(2) + ' Mb';
	}
	if (size >= 1024) {
		return (size / 1024).toFixed(2) + ' Kb';
	}
	return size + ' bytes';
};
var imgPerPage = 12;
var allow_delete = true, url_stored = "/Manage/Stored";;
	$(document).ready(function(){
			var params = {source:'images', sort_name:'created', sort_order:'desc'};
			var pageClick = function(page) {
				//arr = $("input:checked"); 
				//params.source = arr[0].value;
				//params.sort_order = arr[1].value;
				loadImages(page,params);
			};
			loadImages(1, params);

		function loadImages(page, params) {
			$("#rsp-status").html('loading...');
			var r_img_ext = /\.(jpeg|png|gif)$/,
			      f_img_replace = function(s,ext){return "-s160."+ext;};
			$.get('/api/browse/'+page, function(data){
//				log(data);
//				alert("in");
				if (!$.isArray(data.items) || data.items.length == 0) {
					return false;
				}
				var page_count = Math.ceil(data.total/imgPerPage); //log(page_count);
//				alert(page_count);
				if (page_count > 1) {
					$("#pager").pager({ pagenumber: page, pagecount: page_count, buttonClickCallback: pageClick });
				} else {
					$("#pager").empty();
				}

				$("#rsp-status").empty();
				var url_prefix = data.url_prefix ? data.url_prefix : "http://img.free4lab.com/"; //TODO 
				$("#image-list").empty();

				$.each(data.items, function(i, item){//console.log(item);
					var alt = (item.width && item.height) ? (item.width+'x'+item.height) : '', title = item.note ? item.note : '';
					
					if (item.created) {
						alt += '上传时间: ' + item.created;
					}
					var _li = $("<li></li>").attr("id", "li_iid" + item.id).appendTo("#image-list"), 
						_a = $("<a></a>").attr("href", url_prefix + item.filename).attr("title", title+" ( "+alt+" )").attr('rel','box'),
						_img = $("<img/>").attr("src", url_prefix + item.filename.replace(r_img_ext,f_img_replace)).attr('alt',alt).attr("class", ""),
						_txt = $("<span></span>").attr("class", "lbl").attr("title",item.length).text(format_size(item.length)),
						_btn = $("<span></span>").attr("class", "btn btn_delete ui-corner-all ui-icon ui-icon-trash").attr("title", "删除")
							.click(function(){
								if (!confirm("确认要删除此图片么，此操作将不可恢复？")) return false;
								// 删除指定的图片
								var id = $(this).parent().attr("id").substr(6);
								$.post("/api/delete/"+id, function(data) {
									//log(data, $("#li_iid" + id));
									if (data === true) {
										$("#li_iid" + id).fadeOut(function(){$(this).remove();});
									}
									else alertAjaxResult(data);
								}, 'json');

								return false;
							}).hide();
					_a.append(_img).appendTo(_li);//log(_img);
					_txt.appendTo(_li);
					if (allow_delete) {
						_li.append(_btn).hover(function(){
							_btn.fadeIn();
						},function(){
							_btn.fadeOut();
						});
					}
					
				});
				
				// colorbox
				$("#image-list a").colorbox();
				
			}, 'json');
			}


			//$("#radio").buttonset();
			$(".button").button();
			
	});
