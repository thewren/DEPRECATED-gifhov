function borderDragOverDecorate(decoratedElement) {

decoratedElement.addEventListener("dragover", function(event) { event.preventDefault(); }, true);

decoratedElement.addEventListener("dragover", function() { decoratedElement.style.border="2px dashed #bdbdbd"; }, true);

decoratedElement.addEventListener("dragleave", function() { decoratedElement.style.border="1px dashed #bdbdbd"; }, true);

decoratedElement.addEventListener("drop", function() { decoratedElement.style.border="1px dashed #bdbdbd"; }, true);

}

function innerDragOverDecorate(decoratedElement) {
var checkmark = "<i class=\"icon-checkmarkok\"></i>"
decoratedElement.addEventListener("drop", function() { decoratedElement.innerHTML = checkmark; });
}
function gifInnerDragOverDecorateError(decoratedElement) 
{ decoratedElement.innerHTML= "drag a gif"; };

function audioInnerDragOverDecorateError(decoratedElement) 
{ decoratedElement.innerHTML= "drag audio"; };



borderDragOverDecorate(audiosquare);
borderDragOverDecorate(gifsquare);


innerDragOverDecorate(dragGifText);
innerDragOverDecorate(dragAudioText);