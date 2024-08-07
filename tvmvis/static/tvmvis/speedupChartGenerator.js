
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

    console.log(runIds)

    // Convert runIds to a sorted array
    const sortedRunIds = Array.from(runIds).sort((a, b) => a - b);

    // Extract benchmark names and sort them
    const sortedBenchmarks = Object.keys(data).sort((a, b) => {
        const aBase = a.replace(/-\d+$/, '');  // remove the trailing number
        const bBase = b.replace(/-\d+$/, '');  // remove the trailing number
        if (aBase === bBase) {
            const aNum = parseInt(a.match(/-(\d+)$/)[1], 10);  // extract the trailing number
            const bNum = parseInt(b.match(/-(\d+)$/)[1], 10);  // extract the trailing number
            return aNum - bNum;
        }
        return aBase.localeCompare(bBase);
    });

    // Prepare chartData array for Google Charts
    const chartData = [
        ["Benchmark", ...sortedRunIds.flatMap(runId => [`Run${runId}`, { role: 'annotation' }])]
    ];

    sortedBenchmarks.forEach(benchmark => {
        const row = [benchmark];
        sortedRunIds.forEach(runId => {
            const value = data[benchmark][runId] !== undefined ? data[benchmark][runId] : 0;
            row.push(value, value.toString());
        });
        chartData.push(row);
    });

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


        // Add event listener to download button
        document.getElementById('download-chart-button').addEventListener('click', () => {
            const uri = chart.getImageURI();
            const link = document.createElement('a');
            link.href = uri;
            link.download = 'chart.png';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    });
}