console.log('chart.js Loaded')

function drawLineChart(chartData, eleId){
    google.charts.load('current', {packages: ['corechart', 'line']});
    google.charts.setOnLoadCallback(function (){
        var data = google.visualization.arrayToDataTable(chartData);
        var chartElement = document.getElementById(eleId);
        var chart = new google.visualization.LineChart(chartElement);
        chart.draw(data);
    })
}