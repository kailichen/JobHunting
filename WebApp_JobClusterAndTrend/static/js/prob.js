var source = new EventSource('/prob')
source.onmessage = function(event) {
    if (event.data !== 1){
        var prob = parseInt(event.data.slice(15,17));
        console.log(ColorConvert(prob));
        colorx = ColorConvert(prob);
        if (colorx != null){
            map.updateChoropleth({
                "AL": colorx,
"AK": colorx,
"AZ": colorx,
"AR": colorx, 
"CA": colorx,
"CO": colorx,
"CT": colorx,
"DE": colorx,
"FL": colorx,
"GA": colorx,
"HI": colorx,
"ID": colorx,
"IL": colorx,
"IN": colorx,
"IA": colorx,
"KS": colorx,
"KY": colorx,
"LA": colorx,
"ME": colorx,
"MD": colorx,
"MA": colorx,
"MI": colorx,
"MN": colorx,
"MS": colorx,
"MO": colorx,
"MT": colorx,
"NE": colorx,
"NV": colorx,
"NH": colorx,
"NJ": colorx,
"NM": colorx,
"NY": colorx,
"NC": colorx,
"ND": colorx,
"OH": colorx,
"OK": colorx,
"OR": colorx,
"PA": colorx,
"RI": colorx,
"SC": colorx,
"SD": colorx,
"TN": colorx,
"TX": colorx,
"UT": colorx,
"VT": colorx,
"VA": colorx,
"WA": colorx,
"WV": colorx,
"WI": colorx,
"WY": colorx
            });
        }
    }
}

function ColorConvert (o) {
    var Red = 255 - (255 * (o / 100));
    var Green = 255 * (o / 100);
    var Blue = 0;
    console.log(Red==NaN);
    console.log(Green==NaN);
    console.log(Blue==NaN);
    if (!isNaN(Red) && !isNaN(Green) && !isNaN(Blue)){
        return 'rgb(' + Red + ',' + Green + ',' + Blue + ')';
    }
    else{
        return null;
    }
}