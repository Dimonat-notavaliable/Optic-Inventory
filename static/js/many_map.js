var map = L.map('map').setView([56.497, 84.9744], 12);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

map.attributionControl.setPrefix('')

var greenIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

let facilities = JSON.parse(document.getElementById('facilities_json').textContent);

// for each facility, add a Marker
facilities.forEach(facility => {
    var marker = L.marker([facility.latitude, facility.longitude],
        {icon: greenIcon});
    marker.bindPopup(facility.name).openPopup();
    marker.addTo(map);
})