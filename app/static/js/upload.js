function handleFiles(files) {
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
		file.id = 'new_file';
        var imageType = /image.*/;

        if (!file.type.match(imageType)) continue;

        var img = document.createElement("img");
        //img.classList.add("obj");
        img.file = file;
	   var li = $('<li />').addClass('new').append(img);	//alert(li.html());
	   //li.append('<label class="lbl"><input class="new" title="描述" type="text" name="new_description[]" size="18" /></label>');
	   li.append($('<span class="btn" />').addClass('btn ui-corner-all ui-icon ui-icon-trash').attr('title','delete').click(function(){$(this).parent().fadeOut(function(){$(this).remove();});return false;}));
	   $("#image-pic-list").prepend(li);
        var reader = new FileReader();
        reader.onloadend = (function(img) {
			return function(e) { img.src = e.target.result; $(img).attr('title',''+img.naturalWidth+'x'+img.naturalHeight+''); }; 
		})(img);
        reader.readAsDataURL(file);
    }
}

var dropbox, preview, url_stored = "/api/upload";

$(document).ready(function(){
	     //alert("in");
		// init event
		preview = document.getElementById("image-pic-list");
		dropbox = document.getElementById("dropbox");
		window.addEventListener("dragenter", function(e) {
			e.preventDefault();
			dropbox.setAttribute("dragenter", true);
		}, true);
		window.addEventListener("dragleave", function(e) {
			dropbox.removeAttribute("dragenter");
		}, true);
		dropbox.addEventListener("dragover", function(e) {
			e.preventDefault();
		}, false);
		dropbox.addEventListener("drop", function(e) {
			e.preventDefault();
			dropbox.removeAttribute("dragenter");
			var dt = e.dataTransfer;
			var files = dt.files;

			handleFiles(files);
		}, false);

		$("#progressbar").progressbar().hide();
		$("#pic-input").change(function(){
			handleFiles(this.files);
		});
		$("#image-pic-list").sortable({
			//placeholder: 'ui-state-highlight',
			update: function(event, ui) {
				//console.log(event, ui);
			}
		});
		$("#image-pic-list").disableSelection();
		
	    $("#submit_button").click(function(form){
	    	
	    	if ($("#image-pic-list li").length == 0) return false;
			$("#image-pic-list li.new").each(function(i){
				$(this).attr('id','li_new'+i);
			});
			var sorted = $("#image-pic-list").sortable( 'toArray' );
			/*$.each(sorted, function(i, item){
				var res = item.match(/(.+)[-=_](.+)/);
				if(res) params.push({name:'li[]',value:res[2]});
			});*/
			var files = [];
			$("li.new").each(function(i, li){
				var img = $("img", this).get(0);
				if (typeof img.file !== "undefined") files.push(img.file);
			});
			if(files.length > 0) $("#progressbar").show();
			
//			alert(files);
			
			$("#pic-input").html5_upload({
	        	/*
	            url: function(number) {
	                return prompt(number + " url", "/");
	            },*/
	    		files: files,
	    		fieldName: 'file',
	        	url: "/api/upload",
	            sendBoundary: window.FormData || $.browser.mozilla,
	            autostart: false,
	            onStart: function(event, total) {
//	                return confirm("You are trying to upload " + total + " files. Are you sure?");
	                return true;
	            },
	            onProgress: function(event, progress, name, number, total) {
	                console.log(progress, number);
	            },
	            setName: function(text) {
	                $("#progress_report_name").text(text);
	            },
	            setStatus: function(text) {
	                $("#progress_report_status").text(text);
	            },
	            setProgress: function(val) {
	               // $("#progress_report_bar").css('width', Math.ceil(val*100)+"%");
	            	$("#progressbar").progressbar('value',Math.ceil(val*100));
	            },
	            onFinishOne: function(event, response, name, number, total) {
	                //alert(response);
	            },
	            onFinish: function(event,total){
	            	$("#progressbar").progressbar('value',100).fadeOut("slow");
	            },
	            onError: function(event, name, error) {
	                alert('error while uploading file ' + name);
	            }
	        });
			
			$("#pic-input").triggerHandler('html5_upload.start');
			return false;
	    	return true;
	    });
		
	    $("#grab_button").click(function(form){
	    	if($("#pic-url")[0].value.length == 0){
	    		$("#grab_result").html("<p>图片url不能为空</p>");
	    		return false;
	    	}
	    	else{
		    	$.post("/api/url?url=" + $("#pic-url")[0].value, function(data) {
	    		  $("#grab_result").html(data);
	    		},'text');
	    	}
	    });

		$(".button").button();

		$("#clear").click(function(){
			$("#pic-input").val(null);
		});
});
