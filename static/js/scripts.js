// let mapOptions = {
//     center:[-1.284, 36.8181],
//     zoom:10
// }


// let map = new L.map('map' , mapOptions);

// let layer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
// map.addLayer(layer);

// // let customIcon = {
// //     iconUrl:
// // }

// let iconOptions = {
//     title:"Carnect.Ltd",
//     draggable:true,
// }

// let marker = new L.Marker([-1.284, 36.8181], iconOptions);
// marker.addTo(map);
// marker.bindPopUp('content').openPopup();

// let popup = L.popup().setLatLng([-1.284, 36.8181] ).setContent("<p>new popup</br> more complicated</p>").openOn(map);

const DEFAULT_COORD = [-1.284, 36.8181]
const resultsWrapperHTML = document.getElementById("search-result")

// initial map
const Map = L.map("render-map")

// initial osm tile url
const osmTileUrl = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"

const attrib = 'Leaflet with <a href="https://academy.byidmore.com">Id More Academy<a>'

const osmTile = new L.TileLayer(osmTileUrl, { minZoom: 2, maxZoom: 20, attribution: attrib })

// add layer 
// https://leafletjs.com/reference-1.6.0.html#layer
Map.setView(new L.LatLng(DEFAULT_COORD[0], DEFAULT_COORD[1]), 15)
Map.addLayer(osmTile)

// add marker
// https://leafletjs.com/reference-1.6.0.html#marker
const Marker = L.marker(DEFAULT_COORD).addTo(Map)

// click listener
// https://leafletjs.com/reference-1.6.0.html#evented
Map.on("click", function(e){
  const {lat, lng} = e.latlng
  // regenerate marker position
  Marker.setLatLng([lat, lng])
})

// search location handler
let typingInterval 

// typing handler
function onTyping(e) {
  clearInterval(typingInterval)
  const {value} = e
  
  typingInterval = setInterval(() => {
    clearInterval(typingInterval)
    searchLocation(value)
  }, 500)
}

// search handler
function searchLocation(keyword) {
  if(keyword) {
    // request to nominatim api
    fetch(`https://nominatim.openstreetmap.org/search?q=${keyword}&format=json`)
      .then((response) => {
        return response.json()
      }).then(json => {
       // get response data from nominatim
       console.log("json", json)
        if(json.length > 0) return renderResults(json)
        else alert("lokasi tidak ditemukan")
    })
  }
}

// render results
function renderResults(result) {
  let resultsHTML = ""
  
  result.map((n) => {
    resultsHTML += `<li><a href="#" onclick="setLocation(${n.lat},${n.lon})">${n.display_name}</a></li>`
  })
  
  resultsWrapperHTML.innerHTML = resultsHTML
}

// clear results
function clearResults() {
  resultsWrapperHTML.innerHTML = ""
}

// set location from search result
function setLocation(lat, lon) {
  // set map focus
  Map.setView(new L.LatLng(lat, lon), 15)
  
  // regenerate marker position
  Marker.setLatLng([lat, lon])
   
  // clear results
  clearResults()
}

