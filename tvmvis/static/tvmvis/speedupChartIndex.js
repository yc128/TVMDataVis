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





