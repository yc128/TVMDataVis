//Selector Initialization
document.addEventListener('DOMContentLoaded', function () {
    // 查找所有类名为 'auto-init-select' 的 <select> 元素
    let counter = 0;
    document.querySelectorAll('.chart-title-selector').forEach(function(selectElement) {

        // Add option for <select>
        charTitles.forEach(function(optionText) {
            var option = new Option(optionText, optionText);
            selectElement.add(option);
        });
        if(counter < charTitles.length){
            selectElement.value = charTitles[counter];
            updateTable(selectElement);
        }

        counter++;

    });
});

var newChartTitle = []
charTitles.forEach(function (chartTitle) {
    if(typeof charDatas[chartTitle][1][1] === 'number'){
        newChartTitle.push(chartTitle)
    }
})
charTitles = newChartTitle



// drawLineChartByTitle(charDatas, charTitles[0], 'chart_div2');
// updateLineChart(charTitles[1], 'chart_div2');