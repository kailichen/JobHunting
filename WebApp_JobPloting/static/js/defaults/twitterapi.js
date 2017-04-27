// call twitter oembed api to insert html block
function callTweet(tw_id){
    if( typeof tw_id === 'undefined' || tw_id.length < 4){
        $("#innerDiv").html("<p>The Tweet not available to pull from Twitter API. :(</p>");
        return undefined;
    }

    var linkaddr = "https://api.twitter.com/1.1/statuses/oembed.json?id=" + tw_id;
    $.ajax({
            url: linkaddr,
            dataType: "jsonp",
            success: function(data){
                $("#innerDiv").html(data.html);
            },
            error: function(err) {
                console.log("error");
                $("#innerDiv").html("<p>Tweet not available</p>");
            }
        }).always(function(jqXHR, textStatus) {
            if($('#innerDiv').children().length === 0 ){
                console.log("fetch error");
                $("#innerDiv").html("<p>Tweet not available</p>");
            }
        });
}
