function initAutocomplete() {
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 40.7128, lng: -74.0060},
    zoom: 15,
    mapTypeId: 'roadmap'
  });

  // Create the search box and link it to the UI element.
  var input = document.getElementById('pac-input');
  var searchBox = new google.maps.places.SearchBox(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
  function init(){
  const initialPosition = {lat: 40.7128, lng: -74.0060};
  // const map = new google.maps.Map(document.getElementById('map'), {
  //   center: initialPosition,
  //   zoom: 15
  // });
    const marker = new google.maps.Marker({maps, position:initialPosition });
    if ('geolocation' in navigator){
      navigator.geolocation.getCurrentPosition(
        position => console.log(`Lat: ${position.coords.latitude} Lng: ${position.coords.longitude}`),
        err => alert(`Error (${err.code}): ${err.message}`)
      );
    }
    else {
      alert('Geolocation is not supported by your browser.');
    }
    navigator.geolocation.getCurrentPosition(success, error, [options])
    }
    navigator.geolocation.getCurrentPosition(
  // On success
  position => console.log(`Lat: ${position.coords.latitude} Lng: ${position.coords.longitude}`),
  // On error
  err => alert(`Error (${err.code}): ${err.message}`)
);
const getPositionErrorMessage = code => {
  switch (code) {
    case 1:
      return 'Permission denied.';
    case 2:
      return 'Position unavailable.';
    case 3:
      return 'Timeout reached.';
  }
}
}
