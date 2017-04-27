//   map.updateChoropleth({
//     'CA': {'JobHunts': '[asdasd,weqewqe]'}
//   });
var source = new EventSource('/stream')
source.onmessage = function(event) {
    if (event.data !== '1'){
        var key;
        if (event.data.slice(2,4) !== 'nu'){
            key = event.data.slice(2,4);
        var dataJson = JSON.parse(event.data);
        var job = dataJson[key];
        var jobArray = [];
        for (var i = 0; i < job.length; i++){
            jobArray.push(job[i][0]);
        }
        console.log('state to update: ' + key);
        console.log('jobs: ' + jobArray);
        var state_info = {}
        state_info['fillKey'] = 'Probability';
        state_info['JobHunts'] = jobArray;
        var state = {}
        state[key] = state_info;
        map.updateChoropleth(state);
        }
    }
}