var DD_listenerGif = function(type) {
	return function(event) {
		event.preventDefault();
		var droppedobj = event.dataTransfer.files[0];	
		var e = event || window.event;
		var dt    = e.dataTransfer;
		var files = dt.files;
		for (var i=0; i<files.length; i++) {
			var file = files[i];
			var reader = new FileReader();
			
			
			
			
			
			reader.readAsDataURL(file);
		}
		
		if (
		file.type.split('/')[1] == "gif" || 
		file.type.split('/')[1] == "jpg" || 
		file.type.split('/')[1] == "jpeg" || 
		file.type.split('/')[1] == "png" && 
		file.size < 30000000){
		
		gifHovImage.onmouseover = function(){
			audioboom.pause();
		};
			addEventHandler(reader, 'loadend', function(e, file) {
				var bin           = this.result; 
				var newFile       = document.createElement('div');
				
				newFile.innerHTML = 'Loaded : '+file.name+' size '+file.size+' B';
				list.appendChild(newFile);  
				var fileNumber = list.getElementsByTagName('div').length;
				status.innerHTML = fileNumber < files.length 
				? 'Loaded 100% of file '+fileNumber+' of '+files.length+'...' 
				: 'Done loading. processed '+fileNumber+' files.';
				var img = document.getElementsByClassName('sampleImage')[0]; 
				img.file = file;   
				img.src = bin;
			}.bindToEventHandler(file));
			
			form.append(type, droppedobj);
			
			
			
			ok[type] = true;
			sendTheXHR();
		}
		else {
		
		
		gifInnerDragOverDecorateError(dragGifText);
		var gifErrorMessage = document.createElement('div');
		gifErrorMessage.setAttribute("id", "gifErrorMessage");
		gifErrorMessageDiv.innerHTML = 'That\s no gif...';
		gifErrorMessageDiv.style.color="red";
		gifErrorMessageDiv.style.fontSize="11px";
		}; 
	};
};
