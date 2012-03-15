(function($){
    $.fn.print_r = function(json){
        return $(this).each(function(e){
            $(this).html(_print_r(json));
        })
    }
    function _print_r(theObj) {
        var retStr = '';
        if (typeof theObj == 'object') {
            retStr += '<div style="font-size:12px;">';
            for (var p in theObj) {
                if (typeof theObj[p] == 'object') {
                    retStr += '<div><b>['+p+'] => ' + typeof(theObj) + '</b></div>';
                    retStr += '<div style="padding-left:25px;">' + _print_r(theObj[p]) + '</div>';
                } else {
                    retStr += '<div>['+p+'] => <b>' + theObj[p] + '</b></div>';
                }
            }
            retStr += '</div>';
        }
        return retStr;
    }   
    $.print_r = function(json){
        return _print_r(json);
    }
})(jQuery);

$(function() {
    
    
    $("#submit_button").click(function(form){
    	//alert($("#upload_field")[0].files);
    	var files = $("#upload_field")[0].files;
//    	$("#upload_field").html5_upload.start();
    	$("#upload_field").html5_upload({
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
                //return confirm("You are trying to upload " + total + " files. Are you sure?");
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
                $("#progress_report_bar").css('width', Math.ceil(val*100)+"%");
            },
            onFinishOne: function(event, response, name, number, total) {
                alert(response);
            },
            onError: function(event, name, error) {
                alert('error while uploading file ' + name);
            }
        });
    	
    	$("#upload_field").triggerHandler('html5_upload.start');
    	return true;
    });
    
    FlyJSONP.init({debug: true});
    
    $("#test_button").click(function(){ 
	    /*
	    FlyJSONP.get({
      url: 'http://mytest1.free4lab.com/api/browse/6',
      success: function (data) {
      	$("#test_result").print_r(data);
        console.log(data);
      },
      error: function (errorMsg) {
            	alert("in error");
        console.log(errorMsg);
      }
    });*/
    /*
    $.getJSON("http://mytest1.free4lab.com/api/browse/6?callback=?",
  function(data) {
    $("#test_result").print_r(data);
  });
  */

  $.get("http://mytest1.free4lab.com/api/browse/6?callback=?",
  function(data) {
    $("#test_result").print_r(data);
  },'json');
  /*    */
    });
    
     $("#test_button1").click(function(){ 
        //document.domain = "free4lab.com";
       /**/
        FlyJSONP.post({
      url: 'http://mytest1.free4lab.com/api/url',
      parameters: {
      	url: 'http://img3.douban.com/lpic/s6952038.jpg'
      },
      success: function(data) {
        $("#test_result").print_r(data);
        console.log(data);
      }
    });
    
	    /*
	    $.post("http://mytest1.free4lab.com/api/url?url=http://img3.douban.com/lpic/s6952038.jpg&callback=?", function(data) {
	    		  $("#test_result").html(data);
	    		}, 'text');
	     */	
	    /*
	    $.get("/api/browse/1", function(data) {
			  $("#test_result").html(data);
		}, 'text');
		*/
		/*
		FlyJSONP.get({
      url: '/api/browse/1',
      success: function (data) {
      	alert("in");
      	var result = eval("("+data+")");
      	alert(result);
      	$("#test_result").html(data);
        console.log(data);
      },
      error: function (errorMsg) {
            	alert("in error");
        console.log(errorMsg);
      }
    });
    */
    });
    
    $("#test_button2").click(function(){ 
    	//will fail
        alert($("#if")[0].contentDocument.body.textContent);
    });
});
