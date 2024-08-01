document.addEventListener('DOMContentLoaded', function () {
    // Initialize selectors when the DOM is fully loaded
    initializeRunIDChangeListeners();
    initializeGenerateButtonListeners();
});



/**
 * Initialize event listeners for comparison target change.
 */
function initializeRunIDChangeListeners() {
    document.querySelectorAll('.run-id-selector').forEach(selectorElement => {
        const groupLayout = selectorElement.closest('.title-sel-group');

        let bmNameSelectorElement = groupLayout.querySelector('.benchmark-name-container');
        let targetSelectorElement = groupLayout.querySelector('.run-id-selector');

        selectorElement.addEventListener('change', () => {
            updateBenchmarkNameContainer(bmNameSelectorElement, 'byRun', targetSelectorElement.value, targetSelectorElement.value);
        });
    });
}


/**
 * Update benchmark name container with checkboxes based on comparison targets.
 * @param {Element} bmNameContainer - The benchmark name container element.
 * @param {string} compMode - The selected comparison mode.
 * @param {string} compTar1Val - The value of the first comparison target.
 * @param {string} compTar2Val - The value of the second comparison target.
 */
function updateBenchmarkNameContainer(bmNameContainer, compMode, compTar1Val, compTar2Val) {
    bmNameContainer.innerHTML = '';  // Clear previous checkboxes

    const url = new URL('/tvmvis/fetch-benchmark-name-data/', window.location.origin);
    url.searchParams.append('comparisonMode', compMode);
    url.searchParams.append('compareTargets', compTar1Val);
    url.searchParams.append('compareTargets', compTar2Val);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("bm name data:", data);
            // Sort data alphabetically
            data.sort((a, b) => a.localeCompare(b));

            data.forEach(optionText => {
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.value = optionText;
                checkbox.id = `benchmark-${optionText}`;

                const label = document.createElement('label');
                label.htmlFor = checkbox.id;
                label.textContent = optionText;

                const div = document.createElement('div');
                div.appendChild(checkbox);
                div.appendChild(label);

                bmNameContainer.appendChild(div);
            });
        });
}