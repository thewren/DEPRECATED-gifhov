$(function()){
	$ ('#uploads').filedrop({
		url: 'upload.html',
		parameter: 'imagefile',
		fallbackid: 'upload_button',
		maxfiles: 5,
		maxfilesize: 2, 
		
		uploadFinished: function(i,file,response)
		{
		alert(response);
		}
		
		
		});
		});