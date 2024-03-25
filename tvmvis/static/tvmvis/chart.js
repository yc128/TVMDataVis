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


/**
 * Update the chart on given div with given params
 * @param chartTitle
 * @param eleId
 */
function updateLineChart(chartTitle, eleId){
    fetch(`/tvmvis/fetch-data/?yTitle=${chartTitle[0]}&yTitleAdd=${chartTitle[1]}`)
        .then(response => response.json())
        .then(data => {
            // console.log("draw with data:")
            // console.log(data)
            drawLineChartByTitle(data, chartTitle, eleId);
        })
}


function updateTable(selectElement, selectElementAdd) {
    var selectedOption = [];
    selectedOption.push(selectElement.value);
    if(selectElementAdd !== undefined){
        selectedOption.push(selectElementAdd.value);
    }else{
        selectedOption.push("--");
    }

    var groupLayout = selectElement.closest('.chart-group');
    var tableDiv = groupLayout.querySelector('.chart-div');
    // console.log(selectedOption);
    // console.log(tableDiv);

    // 现在你可以更新这个 tableDiv
    // tableDiv.innerHTML = "<p>已选择：" + selectedOption + "</p>";
    updateLineChart(selectedOption, tableDiv.id)
}