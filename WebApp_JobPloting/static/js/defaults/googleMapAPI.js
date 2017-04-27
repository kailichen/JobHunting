'use strict';

var map;
var node = document.createElement('div');
node.innerHTML = '<p data-bind="text: $root.name"></p>';
var contentString = node;
var infowindow;

// Call back function for googleMap AJAX request
function initMap() {
	map = new google.maps.Map(document.getElementById("googleMap"),{
		// initiate map centering at Chicago, show full US
        center: new google.maps.LatLng(41.850033, -87.6500523),
		zoom: 4
	});
	infowindow = new google.maps.InfoWindow({
		content: ''
	});
}

// all markers set up function
function addMapMarkers(markerArray){
    var location;
    var id_apart;
    var id_bpart;
    var id_str;
    var marker;
    markerArray.forEach(function(elem){
        location = new google.maps.LatLng(elem.lat, elem.lng);
        // id_apart = elem.tweetpa;
        // id_bpart = elem.tweetpb;
        // if (typeof id_apart === 'undefined')
        //     id_apart = 0;
        // if (typeof id_bpart === 'undefined')
        //     id_bpart = 0;
        var id_str = elem.id_str;
        if (typeof id_str === 'undefined'){
            id_str = 0;
        }
        marker = new google.maps.Marker({
            map: map,
            position: location,
            opacity: 0.6,
            title: id_str,
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 6,
                fillColor: 'magenta',
                strokeColor: 'magenta'
            }
        });
        // add callback function for each marker click
        google.maps.event.addListener(marker, 'click', (function (marker) {
            return function () {
                infowindow.setContent('<div id = "innerDiv">Loading Tweet ...</div>');
                callTweet(marker["title"]);
                if($('#innerDiv').children().length === 0 ){
                    // console.log("fetch error");
                    $("#innerDiv").html("<p>The Tweet not available to pull from Twitter API. :(</p>");
                }
                infowindow.open(map, marker);
            }
        })(marker));
    });
}
