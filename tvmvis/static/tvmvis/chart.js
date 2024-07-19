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


function drawChartByTitle(chartDatas, compTargetTitles, eleId, chartType, chartTitleList) {
    /**
     * @param chartDatas: dict chartData
     * @param compTargetTitles: keys for extracting data from dict
     * @param chartTitleList: List for chart title: [chartTitle, yTitle, xTitle]
     */
    console.log(compTargetTitles)
    let chartData = chartDatas[compTargetTitles[0]];

    chartData[0][1] = compTargetTitles[0];
    console.log("chartData: "+chartData);
    if (compTargetTitles[1] != "-" && compTargetTitles[1] != "--") {
        let chartDataAdd = chartDatas[compTargetTitles[1]];
        chartDataAdd[0][1] = compTargetTitles[1];
        for (let i = 0; i < chartData.length; i++) {
            chartData[i].push(chartDataAdd[i][1]);
        }
    }

    google.charts.load('current', {packages: ['corechart']});
    google.charts.setOnLoadCallback(function () {
        var data = google.visualization.arrayToDataTable(chartData);
        var chartElement = document.getElementById(eleId);
        var chartOptions = {
            title: chartTitleList[0],
            hAxis: {title: chartTitleList[1]},
            vAxis: {title: chartTitleList[2]},
            legend:{textStyle: {fontSize: 10}}
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

    //Construct the charTitle, X,Y Title
    var chartTitleList = [];
    var chartTitle = comparisonMode + "; Benchmark: "+benchmarkName;
    chartTitleList.push(chartTitle);
    chartTitleList.push(parameterType);

    let compareTargets = []
    if(comparisonMode == "byRun"){
        chartTitleList.push("DeviceName");
        compareTargets = runId;
    }else{
        chartTitleList.push("RunID");
        compareTargets = deviceName;
    }
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("draw with data:")
            console.log(data)
            drawChartByTitle(data, compareTargets, tableDiv.id, 'BarChart', chartTitleList);
        })
}