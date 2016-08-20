var videoMarkers = [];

var map = L.map('map').setView([65,25], 6);

L.tileLayer('http://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}', {
  attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  subdomains: 'abcd',
  minZoom: 1,
  maxZoom: 16,
  ext: 'png'
}).addTo(map);

map.locate({
  setView: true,
  maxZoom: 12
});

var userIcon = L.icon({
  iconUrl: 'person.png',
  iconSize: [24, 48],
  iconAnchor: [12, 48],
  className: 'user-marker'
});

var userMarker = L.marker([65,25], {
  zIndexOffset: 1000,
  icon: userIcon
}).addTo(map);

map.on('locationfound', function(e) {

  userMarker.setLatLng(e.latlng);

  getNearbyVideos();

});

map.on('click', function(e) {

  userMarker.setLatLng(e.latlng);

  getNearbyVideos();

});

document.getElementById('search').addEventListener('keydown', function(e) {
  if (e.keyCode === 13) {
    reqwest({
      url: 'https://search.mapzen.com/v1/autocomplete',
      data: {
        "focus.point.lat": userMarker.getLatLng().lat,
        "focus.point.lon": userMarker.getLatLng().lng,
        text: this.value,
        api_key: "search-rRzXgeF"
      },
      success: function(response) {

        var searchResults = "";

        response.features.forEach(function(address) {

          searchResults = searchResults += "<div class='search-item' data-lat='"+address.geometry.coordinates[1]+"' data-lng='"+address.geometry.coordinates[0]+"'>"+address.properties.label+"</div>";

        });

        document.getElementById("search-results").innerHTML = searchResults;

        var links = document.getElementById("search-results").getElementsByClassName("search-item");

        for (var i = 0; i < links.length; i++) {
          links[i].onclick = function() {

            document.getElementById("search-results").innerHTML = "";

            var clickedCoords = [this.getAttribute('data-lat'), this.getAttribute('data-lng')]

            userMarker.setLatLng(clickedCoords);

            map.setView(clickedCoords);

            getNearbyVideos();

          }
        }

      }
    });
  }
});


function getNearbyVideos() {

  document.getElementById("loading-overlay").style.display = 'block';

  videoMarkers.forEach(function(marker) {
    map.removeLayer(marker);
  });

  reqwest('http://localhost:8080/getData.php?lat='+userMarker.getLatLng().lat+"&lng="+userMarker.getLatLng().lng, function(videos) {

    document.getElementById("loading-overlay").style.display = 'none';

    videos.forEach(function(video) {

      var thumbnailIcon = L.icon({
        iconUrl: video.thumbnail,
        iconSize: [48, 48],
        iconAnchor: [24, 48],
        popupAnchor: [0, -60],
        className: 'video-thumbnail'
      });

      var videoMarker = L.marker(video.location, {icon: thumbnailIcon}).addTo(map);

      videoMarkers.push(videoMarker);

      videoMarker.bindPopup(L.popup({
        minWidth: 180,
        keepInView: true,
        closeButton: false,
        zoomAnimation: false
      }).setContent("<video src='"+video.videoUrl+"' autoplay loop></video>"));

      videoMarker.on('mouseover', function(e) {
        this.openPopup();
      });

      videoMarker.on('mouseout', function(e) {
        this.closePopup();
      });

      videoMarker.on('click', function(e) {
        window.open(video.url);
      });

    });

  });

}