console.log('chart.js Loaded22')

var chartOption = {
    chartArea: {
        width: '70%',
        height: '60%'
    },
    legend: {
        position: 'bottom',
    },
    hAxis: {
        textStyle: {
            fontSize: 7, // 字体大小
        },
        slantedText: true, // 倾斜文本
        slantedTextAngle: 75 // 倾斜角度
    },
}


function drawLineChartByTitle(chartDatas, chartTitle, eleId){
    let chartData = chartDatas[chartTitle[0]];
    if(chartTitle[1] != "-" && chartTitle[1] != "--"){
        let chartDataAdd = chartDatas[chartTitle[1]];
        for(let i = 0; i < chartData.length; i++){
            chartData[i].push(chartDataAdd[i][1]);
        }
    }
    // console.log(chartData);
    google.charts.load('current', {packages: ['corechart', 'line']});
    google.charts.setOnLoadCallback(function (){
        var data = google.visualization.arrayToDataTable(chartData);
        var chartElement = document.getElementById(eleId);
        var chart = new google.visualization.LineChart(chartElement);
        // console.log(data);
        chart.draw(data, chartOption);
    })
}


// /**
//  * Update the chart on given div with given params
//  * @param chartTitle
//  * @param eleId
//  */
// function updateLineChart(chartTitle, eleId){
//     fetch(`/tvmvis/fetch-data/?yTitle=${chartTitle[0]}&yTitleAdd=${chartTitle[1]}`)
//         .then(response => response.json())
//         .then(data => {
//             // console.log("draw with data:")
//             // console.log(data)
//             drawLineChartByTitle(data, chartTitle, eleId);
//         })
// }

/**
 *
 * @param comparisonMode: byRun or byDevice
 * @param parameterType: yTitle
 * @param runId
 * @param deviceName
 */
function updateTable(comparisonMode, parameterType, runId, deviceName) {

    var groupLayout = selectYElement.closest('.chart-group');
    var tableDiv = groupLayout.querySelector('.chart-div');


    const url = new URL('/tvmvis/fetch-data/', window.location.origin);
    url.searchParams.append('comparisonMode', comparisonMode);
    url.searchParams.append('parameterType', parameterType);
    runId.forEach(id => url.searchParams.append('runId', id));
    deviceName.forEach(name => url.searchParams.append('deviceName', name));

    fetch(url)
        .then(response => response.json())
        .then(data => {
            // console.log("draw with data:")
            // console.log(data)
            drawLineChartByTitle(data, chartTitle, tableDiv.id);
        })
}