var newChartTitle = []
charTitles.forEach(function (chartTitle) {
    if(typeof charDatas[chartTitle][1][1] === 'number'){
        newChartTitle.push(chartTitle)
    }
})
charTitles = newChartTitle






//Selector Initialization
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.chart-title-selector-add').forEach(function (selectElement) {
        setSelector(selectElement);
        var option = new Option("-", "-");
        selectElement.add(option);
        selectElement.value = "-";
    })

    // 查找所有类名为 'auto-init-select' 的 <select> 元素
    let counter = 0;
    document.querySelectorAll('.chart-title-selector').forEach(function(selectElement) {
        setSelector(selectElement);
        if(counter < charTitles.length){
            selectElement.value = charTitles[counter];
            updateTable("byRun", "KernelTime",
                [18, 19], ["A", "B"], "montecarlo-2-1024");
        }
        counter++;
    });
});


document.addEventListener('DOMContentLoaded', function() {
    // 为所有 .chart-group 容器中的 <select> 元素添加监听器
    document.querySelectorAll('.title-sel-group').forEach(function(pair) {
        // 获取当前容器中的两个 <select> 元素
        const [select1, selectAdd] = pair.querySelectorAll('select');

        // 为第一个 <select> 添加事件监听器
        select1.addEventListener('change', function() {
            // 当第一个 <select> 发生变化时，执行的逻辑
            // updateTable(select1, selectAdd);
        });

        // 如果你需要，也可以为第二个 <select> 添加监听器
        selectAdd.addEventListener('change', function() {
            // 当第二个 <select> 发生变化时，执行的逻辑
            // updateTable(select1, selectAdd);
        });
    });
});


// drawLineChartByTitle(charDatas, charTitles[0], 'chart_div2');
// updateLineChart(charTitles[1], 'chart_div2');


function setSelector(selectElement) {
    // Add option for <select>
        charTitles.forEach(function(optionText) {
            var option = new Option(optionText, optionText);
            selectElement.add(option);
        });

}