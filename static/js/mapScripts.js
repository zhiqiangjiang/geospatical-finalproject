// Analytics variables
var cData;
var aData;

// Create map
var map = L.map('map').setView([51.049999, -114.066666], 10);

var tiles = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoidG9tamlhbmciLCJhIjoiY2xzd2c5cHl4MnhmeDJtb3c0eG42dnNkNCJ9.giGi3qo495sg__Z9EO1w0w', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
}).addTo(map);

// Overlapping Marker Spiderfier initialization 
var oms = new OverlappingMarkerSpiderfier(map);
var markers = L.markerClusterGroup();

var popup = new L.Popup();
oms.addListener('click', function(marker) {
    popup.setContent(marker.desc);
    popup.setLatLng(marker.getLatLng());
    map.openPopup(popup);
})

oms.addListener('spiderfy', function(markers) {
    map.closePopup();
});

// Color Icons for markers
var redIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var blueIcon = new L.Icon({
    // iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
    iconUrl: 'https://cdn0.iconfinder.com/data/icons/security-double-colour-blue-black-vol-1/52/camera__record__security__cctv-256.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [41, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var greenIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

// Create Traffic Camera Point
function createTC(lat, lng, desc, camurl, camloc, quadrant){
    var loc = new L.LatLng(lat, lng);
    var marker = new L.Marker(loc, {icon: blueIcon});
    var photo = '<img src="'+ camurl +'" style="width:252px;height:189px;">';
    var description = desc + "<br> Location: " + camloc + "<br> Quadrant: " + quadrant + "<br>" + photo;
    marker.desc = description;
    markers.addLayer(marker);
    oms.addMarker(marker);
}

// Create Official Traffic Incident Point
function createTI(lat, lng, info, desc, startdt, quadrant){
    var loc = new L.LatLng(lat, lng);
    var marker = new L.Marker(loc, {icon: redIcon});
    var description = "Type: " + desc + "<br> Location: " + info + "<br> Start DateTime: " + startdt + "<br> Quadrant: " + quadrant;
    marker.bindPopup(description);
    marker.addTo(map);

}

// Create Volunteer Traffic Incident Point
function createVI(lat, lng, info, desc, startdt, quadrant,photoname){
    var loc = new L.LatLng(lat, lng);
    var marker = new L.Marker(loc, {icon: greenIcon});
    // var photo = '<img src="'+ camurl +'" style="width:252px;height:189px;">';
    const staticUrlPrefix = '/static/uploads/';
    var photo = '<img src="' + staticUrlPrefix + photoname + '" style="width:252px;height:189px;">';
    // console.log(photo);
    // var description = "Type: " + desc + "<br> Location: " + info + "<br> Start DateTime: " + startdt + "<br> Upload User: " + quadrant;
    var description = "Type: " + desc + "<br> Location: " + info + "<br> Start DateTime: " + startdt + "<br> Upload User: " + quadrant+ "<br>" + photo;
    marker.bindPopup(description);
    marker.addTo(map);

    

}

//Get today's datetime
function getToday(){
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();

    if(month.toString().length == 1) {
        month = '0'+month;
    }    

    if(day.toString().length == 1) {
        day = '0'+day;
    }

    var datetime = year + "-" + month + "-" + day;

    return datetime;
}

//Get yesterday's datetime
function getYesterday(){
    var date = new Date();
    var yesterday = new Date(date);
    yesterday.setDate(yesterday.getDate()-1);
    var year = yesterday.getFullYear();
    var month = yesterday.getMonth() + 1;
    var day = yesterday.getDate();

    if(month.toString().length == 1) {
        month = '0'+month;
    }    

    if(day.toString().length == 1) {
        day = '0'+day;
    }

    var datetime = year + "-" + month + "-" + day;

    return datetime;
}

// Get today (analytics)
function getTodayA(){
    var date = new Date();
    var month = date.getMonth() + 1;
    var day = date.getDate();

    if(month.toString().length == 1) {
        month = '0'+month;
    }    

    if(day.toString().length == 1) {
        day = '0'+day;
    }

    var datetime = month + "-" + day;

    return datetime;
}

// Get yesterday (analytics)
function getYesterdayA(){
    var date = new Date();
    var yesterday = new Date(date);
    yesterday.setDate(yesterday.getDate()-1);
    var month = yesterday.getMonth() + 1;
    var day = yesterday.getDate();

    if(month.toString().length == 1) {
        month = '0'+month;
    }    

    if(day.toString().length == 1) {
        day = '0'+day;
    }

    var datetime = month + "-" + day;

    return datetime;
}

// Populate map with points
function populateMap(){
    var urlTI = "https://data.calgary.ca/resource/35ra-9556.json";
    var urlTC = "https://data.calgary.ca/resource/k7p9-kppz.json";

    // Read traffic camera json
    fetch(urlTC)
    .then(res=>res.json())
    .then(data=>{
        data.forEach(feature => {
            createTC(feature.point.coordinates[1], feature.point.coordinates[0], feature.camera_url.description, feature.camera_url.url,
                 feature.camera_location, feature.quadrant);
        });
    });

    // Read traffic incident json
    fetch(urlTI)
    .then(res2=>res2.json())
    .then(data2=>{
        data2.forEach(obj => {
            var date = obj.start_dt;
            var today = getToday();
            var yesterday = getYesterday();
            if(date.indexOf(today) > -1) {
                // date contains today
                //console.log("Incident " + obj.id + " occurred today.");
                createTI(obj.point.coordinates[1], obj.point.coordinates[0], obj.incident_info, obj.description, obj.start_dt, obj.quadrant);
            }
        });
    });
    // createTI(51.049999, -114.066666, "Incident Info", "Description", "2023-01-01T00:00:00", "NE");
    $.ajax({
        type: "GET",
        url: "/api/positions", // Your server-side endpoint that fetches positions
        dataType: "json",
        success: function(data) {
            console.log("Successfully fetched DB positions: ", data);
            data.forEach(function(position) {
                createVI(position.latitude, position.longitude, position.location, position.description, position.timestamp, position.user, position.photoname);
            });
        },
        error: function(error) {
            console.error("Error fetching DB positions: ", error);
        }
    });
    map.addLayer(markers);
}

// Refresh map button
function refreshMap(){
    map.closePopup();
    map.eachLayer(function(layer) {
        if(!!layer.toGeoJSON) {
            map.removeLayer(layer);
        }
    });
    oms.clearMarkers();
    markers.clearLayers();
    populateMap();
    map.flyTo(new L.LatLng(51.049999, -114.066666), 10);
}

// Auto refresh map after every 10 minutes
async function autoRefresh(){
    // aData = await fetchAnalytics();
    // cData = await fetchCurrent();

    map.eachLayer(function(layer) {
        if(!!layer.toGeoJSON) {
            map.removeLayer(layer);
        }
    });
    oms.clearMarkers();
    markers.clearLayers();
    populateMap();
   // reportAnalytics();
    setTimeout(autoRefresh, 600000);
}

// fetch database result from py file
async function fetchAnalytics() {
    const url = '/analytics';
    let response = await fetch(url);
    let data = await response.json();
    return data;
}

// fetch current incident results
async function fetchCurrent(){
    const url = 'https://data.calgary.ca/resource/35ra-9556.json';
    let response = await fetch(url);
    let data = await response.json();
    return data;
}

// report analytics section 
function reportAnalytics() {
    var accidents = 0;
    var accidentsne = 0;
    var accidentsnw = 0;
    var accidentsse = 0;
    var accidentssw = 0;

    for(var obj of cData) {
        date = obj.start_dt;
        var today = getTodayA();
        if((date.indexOf(today) > -1)) {
            accidents++;
            if(obj.quadrant=="NE") {
                accidentsne++;
            } else if(obj.quadrant=="NW") {
                accidentsnw++;
            } else if(obj.quadrant=="SE") {
                accidentsse++;
            } else if(obj.quadrant=="SW") {
                accidentssw++;
            }
        }
    }

    var change = percentIncrease(aData.accidents, accidents);
    if(change < 0){
        document.getElementById("changeperc").innerHTML = "There are " + change + "% incidents today than in 2023.";  
    } else if (change > 0) {
        document.getElementById("changeperc").innerHTML = "There are +" + change + "% incidents today than in 2023."; 
    } else {
        document.getElementById("changeperc").innerHTML = "There are the same number of incidents today when compared to 2023"; 
    }
    document.getElementById("canalyticsmsg").innerHTML = "<strong>Number of Incidents: </strong>" + accidents;
    document.getElementById("cneaccidents").innerHTML = "<strong>Incidents in the NE Quadrant: </strong>" + accidentsne;
    document.getElementById("cnwaccidents").innerHTML = "<strong>Incidents in the NW Quadrant: </strong>" + accidentsnw;
    document.getElementById("cseaccidents").innerHTML = "<strong>Incidents in the SE Quadrant: </strong>" + accidentsse;
    document.getElementById("cswaccidents").innerHTML = "<strong>Incidents in the SW Quadrant: </strong>" + accidentssw;
    document.getElementById("analyticsmsg").innerHTML = "<strong>Number of Incidents: </strong>" + aData.accidents;
    document.getElementById("neaccidents").innerHTML = "<strong>Incidents in the NE Quadrant: </strong>" + aData.accidentsNE;
    document.getElementById("nwaccidents").innerHTML = "<strong>Incidents in the NW Quadrant: </strong>" + aData.accidentsNW;
    document.getElementById("seaccidents").innerHTML = "<strong>Incidents in the SE Quadrant: </strong>" + aData.accidentsSE;
    document.getElementById("swaccidents").innerHTML = "<strong>Incidents in the SW Quadrant: </strong>" + aData.accidentsSW;
}

// Perform percent increase calculations
function percentIncrease(x, y){
    result = ((y - x)/Math.abs(x)) * 100;
    return result;
}

autoRefresh();


// function getLocationAndSubmit(formId) {
//     var form = document.getElementById(formId);

//     if (navigator.geolocation) {
//         navigator.geolocation.getCurrentPosition(function(position) {
//             var latitudeInput = form.querySelector('#latitude');
//             var longitudeInput = form.querySelector('#longitude');

//             latitudeInput.value = position.coords.latitude;
//             longitudeInput.value = position.coords.longitude;

//             form.submit();
//         });
//     } else {
//         alert("Geolocation is not supported by this browser.");
//     }
// }
// Saves and stores scroll location so it doesn't reset after page refresh
// window.addEventListener('scroll',function() {
//     // When scroll change, you save it on localStorage.
//     localStorage.setItem('scrollPosition',window.scrollY);
// },false);

// window.addEventListener('load',function() {
//     if(localStorage.getItem('scrollPosition') !== null)
//        window.scrollTo(0, localStorage.getItem('scrollPosition'));
// },false);