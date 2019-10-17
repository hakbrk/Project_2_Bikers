

function buildCharts(year) {

    var chartsURL = "/samples/" + year;
    d3.json(chartsURL).then(function(data) {
    
        var data = [{
            values: data.Counts,
            labels: data.Membership,
            hovertext: data.labels,
            type: 'pie',
        }];

        var layout = {
            showlegend: true,
        };

        Plotly.newPlot('pie', data, layout);

        
    }
    
    )
}



function init() {
//Grab a reference to the dropdown select element
var selector = d3.select("#selDataset");

d3.json("/names").then((yearNames) => {
    yearNames.forEach((year) => {
        selector
            .append("option")
            .text(year)
            .property("value", year);
    });

const firstSample = yearNames[0];
buildCharts(firstSample);

});

}

function optionChanged(newYear) {
buildCharts(newYear);
}

//Initialize the dashboard
init();

