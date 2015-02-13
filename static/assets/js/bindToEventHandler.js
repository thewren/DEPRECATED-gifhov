Function.prototype.bindToEventHandler = function bindToEventHandler() {
  var handler = this;
  var boundParameters = Array.prototype.slice.call(arguments);
  //create closure
  return function(e) {
      e = e || window.event; // get window.event if e argument missing (in IE)   
      boundParameters.unshift(e);
      handler.apply(this, boundParameters);
  }
};
