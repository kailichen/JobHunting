var source = new EventSource('/stream');

source.onmessage = function(event){

    if (event.data!== '1'){
        dataJson = JSON.parse(event.data);
        if ('id' in dataJson){
            if ('geo' in dataJson){
                if ('coordinates' in dataJson["geo"]){
                    // console.log(dataJson);
                    var datamodel = [{
                        "id_str": dataJson["id_str"],
                        "lat": dataJson["geo"]["coordinates"][0],
                        "lng": dataJson["geo"]["coordinates"][1]
                    }];
                    console.log((datamodel)[0].id_str);
                    addMapMarkers(datamodel);
                }
            }
        }
    }
}
