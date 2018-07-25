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
  const map = new google.maps.Map(document.getElementById('map'), {
    center: initialPosition,
    zoom: 15
  });
    const marker = new google.maps.Marker({maps, position:initialPosition });
    if ('geolocation' in navigator){
      navigator.geolocation.getCurrentPosition(
        position => console.log(`Lat: ${position.coords.latitude}) Lng: ${position.coords.longitude}`),
        err => alert(`Error (${err.code}): ${err.message}`)
      );
    } else {
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

const trackLocation = ({ onSuccess, onError = () => { } }) => {
  if ('geolocation' in navigator === false) {
    return onError(new Error('Geolocation is not supported by your browser.'));
  }

  // Use watchPosition instead.
  return navigator.geolocation.watchPosition(onSuccess, onError);
};

function init() {
  const initialPosition = { lat: 59.325, lng: 18.069 };
  const map = createMap(initialPosition);
  const marker = createMarker({ map, position: initialPosition });

  // Use the new trackLocation function.
  trackLocation({
    onSuccess: ({ coords: { latitude: lat, longitude: lng } }) => {
      marker.setPosition({ lat, lng });
      map.panTo({ lat, lng });
    },
    onError: err =>
      alert(`Error: ${getPositionErrorMessage(err.code) || err.message}`)
  });
}

  // Omitted for brevity

  return navigator.geolocation.watchPosition(onSuccess, onError, {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0
  });
};
  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', function() {
    searchBox.setBounds(map.getBounds());
  });

  var markers = [];

  searchBox.addListener('places_changed', function() {
    var places = searchBox.getPlaces();
    console.log("Places returned");

    if (places.length == 0) {
      return;
    }

    // Clear out the old markers.
    markers.forEach(function(marker) {
      marker.setMap(null);
    });
    markers = [];

    // For each place, get the icon, name and location.
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function(place) {
      if (!place.geometry) {
        console.log("Returned place contains no geometry");
        return;
      }
      var image = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25)
      };
      document.getElementById("mapsInfo").addEventListner("click",dis)

      // Create a marker for each place.
      markers.push(new google.maps.Marker({
        map: map,
        // icon: icon
        title: place.name,
        position: place.geometry.location
      }));

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });

  });
