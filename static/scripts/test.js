

var navbar = document.getElementById('navbar');


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

    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function() {
      searchBox.setBounds(map.getBounds());
    });

    var markers = [];

    searchBox.addListener('places_changed', function() {
      var places = searchBox.getPlaces();

      if (places.length == 0) {
        return;
      }
      if (places.length==1) {
        map.setCenter(places[0].geometry.location)
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
        var icon = {
          url: place.icon,
          size: new google.maps.Size(71, 71),
          origin: new google.maps.Point(0, 0),
          anchor: new google.maps.Point(17, 34),
          scaledSize: new google.maps.Size(25, 25)
        };
        //create an info object, add a listener to the marker, so when clicked opens up info window
        // Create a marker for each place.
        var infowindow;
        var marker;
        infowindow = new google.maps.InfoWindow();
        marker = new google.maps.Marker({
          map: map,
          icon: icon,
          title: place.name,
          position: place.geometry.location
        })
        markers.push(marker);
        google.maps.event.addListener(marker, 'click', function() {
          console.log(place);
         infowindow.setContent('<div style = "text-align:center;"><strong>' +  place.name + '</strong><br>' + place.formatted_address + '<br><a class="mapbutton" href="https://www.google.com/maps/search/?api=1&query=' + encodeURI(place.formatted_address) + '">View on Google Maps</a></div>')
         infowindow.open(map, this);
          var latLng = marker.getPosition();
          map.setCenter(latLng);});

        if (place.geometry.viewport) {
          // Only geocodes have viewport.
          bounds.union(place.geometry.viewport);
        } else {
          bounds.extend(place.geometry.location);
        }
      });

    });

  }
