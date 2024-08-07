document.addEventListener('DOMContentLoaded', function () {
    // Initialize selectors when the DOM is fully loaded
    initializeRunIDChangeListeners();
    initializeDeviceSelector();
    initializeGenerateButtonListeners();

    document.querySelectorAll('.run-id-container').forEach(container=>{
        console.log("container")
        updateTargetSelector(container, 'byRun');
    })
});






/**
 * Update target selector options based on the selected comparison mode.
 * @param {Element} targetContainerElement - The target selector element.
 * @param {string} comparisonMode - The selected comparison mode.
 */
function updateTargetSelector(targetContainerElement, comparisonMode) {
    // Clear previous options
    targetContainerElement.innerHTML = '';

    // Fetch new options based on the comparison mode
    const url = new URL('/tvmvis/fetch-relative-mode-data/', window.location.origin);
    url.searchParams.append('comparisonMode', comparisonMode);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("relative mode data:", data);
            addDataToContainer(targetContainerElement, 'RunID', data);
        });
}



/**
 * Initialize event listeners for comparison target change.
 */
function initializeRunIDChangeListeners() {
    document.querySelectorAll('.run-id-container').forEach(selectorElement => {
        const groupLayout = selectorElement.closest('.title-sel-group');

        let bmNameContainerElement = groupLayout.querySelector('.benchmark-name-container');
        let targetContainerElement = groupLayout.querySelector('.run-id-container');


        targetContainerElement.addEventListener('change', () => {
            let selectedRunID = Array.from(targetContainerElement.querySelectorAll('input[type="checkbox"]:checked')).map(input => input.value);
            console.log(selectedRunID)
            updateBenchmarkNameContainer(bmNameContainerElement, 'byRun', selectedRunID);
        });
    });
}


/**
 * Update benchmark name container with checkboxes based on comparison targets.
 * @param {Element} bmNameContainer - The benchmark name container element.
 * @param {string} compMode - The selected comparison mode.
 * @param {Array} compTarVals - The array of value of the first comparison target.
 */
function updateBenchmarkNameContainer(bmNameContainer, compMode, compTarVals) {
    bmNameContainer.innerHTML = '';  // Clear previous checkboxes

    const url = new URL('/tvmvis/fetch-benchmark-name-data/', window.location.origin);
    url.searchParams.append('comparisonMode', compMode);
    compTarVals.forEach(id => url.searchParams.append('compareTargets', id));
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("bm name data:", data);
            addDataToContainer(bmNameContainer, 'benchmark', data);
        });
}


function addDataToContainer(container, idName, data){
    if(data.length > 0 && !Array.isArray(data[0])){
        data.sort((a, b) => a.localeCompare(b));
    }


    data.forEach(singleData => {
        let optionValue = "";
        let optionText = "";
        if(Array.isArray(singleData)){
            optionValue = singleData[0];
            optionText = "id:"+singleData[0]+"; Date:"+singleData[1]+"; CommitPoint:"+singleData[2];

        }else{
            optionText = singleData
            optionValue = singleData
        }
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = optionValue;
        checkbox.id = `${idName}-${optionValue}`;

        const label = document.createElement('label');
        label.htmlFor = checkbox.id;
        label.textContent = optionText;

        const div = document.createElement('div');
        div.appendChild(checkbox);
        div.appendChild(label);

        container.appendChild(div);
    });
}

function initializeDeviceSelector() {
    document.querySelectorAll('.device-name-selector').forEach(selector=>{
        const url = new URL('/tvmvis/fetch-relative-mode-data/', window.location.origin);
        url.searchParams.append('comparisonMode', 'byDevice');
        fetch(url)
            .then(response => response.json())
            .then(data => {
                console.log("device data:", data);
                data.forEach(device =>{
                    const option = new Option(device, device);
                    selector.add(option);
                })
            });
    })

}


function initializeGenerateButtonListeners() {
    document.querySelectorAll('.generate-button').forEach(ButtonElement => {
        ButtonElement.addEventListener('click', () => {
            console.log("Start Generate");
            const groupLayout = ButtonElement.closest('.title-sel-group');
            const bmNames = Array.from(groupLayout.querySelectorAll('.benchmark-name-container input[type="checkbox"]:checked')).map(input => input.value);
            const runIds = Array.from(groupLayout.querySelectorAll('.run-id-container input[type="checkbox"]:checked')).map(input => input.value);
            const deviceName = groupLayout.querySelector('.device-name-selector').value;

            updateSpeedupTable(ButtonElement, runIds, deviceName, bmNames);
        });
    });
}



function updateSpeedupTable(selectElement, runIds, deviceName, benchmarkNames) {

    //Use Selector to find its table div
    const groupLayout = selectElement.closest('.chart-group');
    const tableDiv = groupLayout.querySelector('.chart-div');

    //Add param to url
    const url = new URL('/tvmvis/fetch-speedup-chart-data/', window.location.origin);
    runIds.forEach(id => url.searchParams.append('runIds', id));
    benchmarkNames.forEach(bm => url.searchParams.append('bmNames', bm));
    url.searchParams.append('deviceName', deviceName);

    // Fetch
    fetch(url)
        .then(response => response.json())
        .then(data => {
            drawChart(data, tableDiv)
        })


}


/**
 * Convert the fetched data to Google Charts format and draw the chart
 * @param {Object} data - The data fetched from the server
 * @param {Element} chartDiv - The div element to draw the chart in
 */
function drawChart(data, chartDiv) {
    // Extract runIds dynamically from data
    const runIds = new Set();
    for (const benchmark in data) {
        for (const runId in data[benchmark]) {
            runIds.add(runId);
        }
    }

    // Convert runIds to a sorted array
    const sortedRunIds = Array.from(runIds).sort((a, b) => a - b);

    // Prepare chartData array for Google Charts
    const chartData = [
        ["Benchmark", ...sortedRunIds.flatMap(runId => [`Run${runId}`, { role: 'annotation' }])]
    ];

    for (const benchmark in data) {
        if (data.hasOwnProperty(benchmark)) {
            const row = [benchmark];
            for (const runId of sortedRunIds) {
                const value = data[benchmark][runId] !== undefined ? data[benchmark][runId] : 0;
                row.push(value, value.toString());
            }
            chartData.push(row);
        }
    }

    // Load Google Charts
    google.charts.load('current', { packages: ['corechart', 'bar'] });
    google.charts.setOnLoadCallback(() => {
        const dataTable = google.visualization.arrayToDataTable(chartData);

        const options = {
            title: 'Benchmark Speedup',
            hAxis: { title: 'Benchmark' },
            vAxis: { title: 'Speedup' },
            legend: { position: 'top', maxLines: 3 },
            bar: { groupWidth: '75%' },
            isStacked: false,
            annotations: {
                alwaysOutside: true,
                textStyle: {
                    fontSize: 10,
                    auraColor: 'none',
                    color: '#555'
                }
            },
            tooltip: { isHtml: true }
        };

        const chart = new google.visualization.ColumnChart(chartDiv);
        chart.draw(dataTable, options);
    });
}