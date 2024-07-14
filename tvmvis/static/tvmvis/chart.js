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


function drawChartByTitle(chartDatas, chartTitle, eleId, chartType) {
    /**
     * @param chartDatas: dict chartData
     * @param chartTitle: keys for extracting data from dict
     */
    let chartData = chartDatas[chartTitle[0]];
    console.log("chartData: "+chartData);
    if (chartTitle[1] != "-" && chartTitle[1] != "--") {
        let chartDataAdd = chartDatas[chartTitle[1]];
        for (let i = 0; i < chartData.length; i++) {
            chartData[i].push(chartDataAdd[i][1]);
        }
    }

    google.charts.load('current', {packages: ['corechart']});
    google.charts.setOnLoadCallback(function () {
        var data = google.visualization.arrayToDataTable(chartData);
        var chartElement = document.getElementById(eleId);
        var chartOptions = {
            title: chartType === 'LineChart' ? 'Line Chart' : 'Bar Chart',
            hAxis: {title: 'X Axis Title'},
            vAxis: {title: 'Y Axis Title'}
        };

        var chart;
        if (chartType === 'LineChart') {
            chart = new google.visualization.LineChart(chartElement);
        } else if (chartType === 'BarChart') {
            chartOptions.bars = 'horizontal';  // Required for Material Bar Charts
            chart = new google.visualization.BarChart(chartElement);
        }

        chart.draw(data, chartOptions);
    });
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
function updateTable(selectElement, comparisonMode, parameterType, runId, deviceName, benchmarkName) {

    //Use Selector to find its table div
    const groupLayout = selectElement.closest('.chart-group');
    const tableDiv = groupLayout.querySelector('.chart-div');


    const url = new URL('/tvmvis/fetch-data/', window.location.origin);
    url.searchParams.append('comparisonMode', comparisonMode);
    url.searchParams.append('parameterType', parameterType);
    url.searchParams.append('benchmarkName', benchmarkName);
    runId.forEach(id => url.searchParams.append('runId', id));
    deviceName.forEach(name => url.searchParams.append('deviceName', name));

    var chartTitle = comparisonMode + "; "+benchmarkName;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("draw with data:")
            console.log(data)
            drawChartByTitle(data, runId, tableDiv.id, 'BarChart');
        })
}