console.log('chart.js Loaded2')



function drawLineChartByTitle(chartDatas, chartTitle, eleId){
    chartData = chartDatas[chartTitle]
    // console.log(chartData)
    google.charts.load('current', {packages: ['corechart', 'line']});
    google.charts.setOnLoadCallback(function (){
        var data = google.visualization.arrayToDataTable(chartData);
        var chartElement = document.getElementById(eleId);
        var chart = new google.visualization.LineChart(chartElement);
        chart.draw(data);
    })
}

// function drawLineChart(chartData, eleId){
//     // console.log(chartData)
//     google.charts.load('current', {packages: ['corechart', 'line']});
//     google.charts.setOnLoadCallback(function (){
//         var data = google.visualization.arrayToDataTable(chartData);
//         var chartElement = document.getElementById(eleId);
//         var chart = new google.visualization.LineChart(chartElement);
//         chart.draw(data);
//     })
// }

/**
 * Update the chart on given div with given params
 * @param chartTitle
 * @param eleId
 */
function updateLineChart(chartTitle, eleId){
    fetch(`/tvmvis/fetch-data/?yTitle=${chartTitle}`)
        .then(response => response.json())
        .then(data => {
            drawLineChartByTitle(data, chartTitle, eleId);
        })
}