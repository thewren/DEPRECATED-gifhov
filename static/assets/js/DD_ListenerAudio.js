var DD_listenerAudio = function(type) {
	return function(event) {
		event.preventDefault();
		var droppedobj = event.dataTransfer.files[0];	
		e = event || window.event;
		var dt    = e.dataTransfer;
		var files = dt.files;
		for (var i=0; i<files.length; i++) {
				var file = files[i];
				var reader = new FileReader();
				reader.readAsDataURL(file);
			}
	
		if (
		file.type.split('/')[1] == "mp3" ||
		file.type.split('/')[1] == "m4a" ||
		file.type.split('/')[1] == "x-m4a" ||
		file.type.split('/')[1] == "ogg" && 
		file.size < 30000000){
		
		form.append(type, droppedobj);
		ok[type] = true;
		sendTheXHR();
		}
		else {
		audioInnerDragOverDecorateError(dragAudioText);
		var audioErrorMessage = document.createElement('div');
		audioErrorMessage.setAttribute("id", "audioErrorMessage");
		audioErrorMessageDiv.innerHTML = 'That\'s no audio...';
		audioErrorMessageDiv.style.color="red";
		audioErrorMessageDiv.style.fontSize="11px";		
		};
	
		
};
};
