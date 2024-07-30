document.addEventListener('DOMContentLoaded', function () {
    // Initialize selectors when the DOM is fully loaded
    initializeSelectors();
    initializeComparisonModeChangeListeners();
    initializeComparisonTargetChangeListeners();
    initializeGenerateButtonListeners();
});

/**
 * Initialize comparison mode and parameter selectors.
 */
function initializeSelectors() {
    document.querySelectorAll('.comparison-mode-selector').forEach(selectorElement => {
        setSelector(selectorElement, ["byRun", "byDevice"]);
    });

    document.querySelectorAll('.parameter-selector').forEach(selectorElement => {
        fetchParameterTypes(selectorElement);
    });

    document.querySelectorAll('.comparison-mode-selector').forEach(selectorElement => {
        const groupLayout = selectorElement.closest('.title-sel-group');
        let targetSelectorElement = groupLayout.querySelector('.comparison-target-selector');
        updateTargetSelector(targetSelectorElement, selectorElement.value);

        let targetSelectorElementCompare = groupLayout.querySelector('.comparison-target-selector-compared');
        updateTargetSelector(targetSelectorElementCompare, selectorElement.value);
    });
}

/**
 * Fetch and set parameter types for the parameter selector.
 * @param {Element} selectorElement - The parameter selector element.
 */
function fetchParameterTypes(selectorElement) {
    const url = new URL('/tvmvis/fetch-param-types-data/', window.location.origin);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("param types data:", data);
            data.forEach(optionText => {
                const option = new Option(optionText, optionText);
                selectorElement.add(option);
            });
        });
}

/**
 * Initialize event listeners for comparison mode change.
 */
function initializeComparisonModeChangeListeners() {
    document.querySelectorAll('.comparison-mode-selector').forEach(selectorElement => {
        const groupLayout = selectorElement.closest('.title-sel-group');
        selectorElement.addEventListener('change', () => {
            let targetSelectorElement = groupLayout.querySelector('.comparison-target-selector');
            updateTargetSelector(targetSelectorElement, selectorElement.value);

            let targetSelectorElementCompare = groupLayout.querySelector('.comparison-target-selector-compared');
            updateTargetSelector(targetSelectorElementCompare, selectorElement.value);
        });
    });
}

/**
 * Initialize event listeners for comparison target change.
 */
function initializeComparisonTargetChangeListeners() {
    document.querySelectorAll('.comparison-target-selector, .comparison-target-selector-compared').forEach(selectorElement => {
        const groupLayout = selectorElement.closest('.title-sel-group');

        let bmNameSelectorElement = groupLayout.querySelector('.benchmark-name-selector');
        let targetSelectorElement = groupLayout.querySelector('.comparison-target-selector');
        let targetSelectorElementCompare = groupLayout.querySelector('.comparison-target-selector-compared');
        let compModeElement = groupLayout.querySelector('.comparison-mode-selector');

        selectorElement.addEventListener('change', () => {
            const compMode = compModeElement.value;
            updateBenchmarkNameSelector(bmNameSelectorElement, compMode, targetSelectorElement.value, targetSelectorElementCompare.value);
        });
    });
}

/**
 * Initialize event listeners for generate button click.
 */
function initializeGenerateButtonListeners() {
    document.querySelectorAll('.generate-button').forEach(ButtonElement => {
        ButtonElement.addEventListener('click', () => {
            console.log("Start Generate");
            const groupLayout = ButtonElement.closest('.title-sel-group');
            const bmName = groupLayout.querySelector('.benchmark-name-selector').value;
            const target = groupLayout.querySelector('.comparison-target-selector').value;
            const targetCompared = groupLayout.querySelector('.comparison-target-selector-compared').value;
            const compMode = groupLayout.querySelector('.comparison-mode-selector').value;
            const paramType = groupLayout.querySelector('.parameter-selector').value;

            let runIds = [];
            let deviceNames = [];
            if (compMode === "byRun") {
                runIds.push(target, targetCompared);
            } else {
                deviceNames.push(target, targetCompared);
            }
            updateTable(ButtonElement, compMode, paramType, runIds, deviceNames, bmName);
        });
    });
}

/**
 * Add options to a selector.
 * @param {Element} selectElement - The selector element.
 * @param {Array} options - The list of options to add.
 */
function setSelector(selectElement, options) {
    options.forEach(optionText => {
        const option = new Option(optionText, optionText);
        selectElement.add(option);
    });
}

/**
 * Update target selector options based on the selected comparison mode.
 * @param {Element} targetSelectorElement - The target selector element.
 * @param {string} comparisonMode - The selected comparison mode.
 */
function updateTargetSelector(targetSelectorElement, comparisonMode) {
    // Clear previous options
    while (targetSelectorElement.options.length > 0) {
        targetSelectorElement.remove(0);
    }

    // Fetch new options based on the comparison mode
    const url = new URL('/tvmvis/fetch-relative-mode-data/', window.location.origin);
    url.searchParams.append('comparisonMode', comparisonMode);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("relative mode data:", data);
            data.forEach(runDetail => {
                console.log("RunDetail"+runDetail)
                let optionText = "RunID:"+runDetail[0]+"-DateTime:"+runDetail[1]+"-CommitPoint:"+runDetail[2];
                const option = new Option(optionText, runDetail[0]);
                targetSelectorElement.add(option);
            });
        });
}

/**
 * Update benchmark name selector options based on comparison targets.
 * @param {Element} bmNameSelectorElement - The benchmark name selector element.
 * @param {string} compMode - The selected comparison mode.
 * @param {string} compTar1Val - The value of the first comparison target.
 * @param {string} compTar2Val - The value of the second comparison target.
 */
function updateBenchmarkNameSelector(bmNameSelectorElement, compMode, compTar1Val, compTar2Val) {
    // Clear previous options
    while (bmNameSelectorElement.options.length > 0) {
        bmNameSelectorElement.remove(0);
    }

    // Fetch new options based on the comparison targets
    const url = new URL('/tvmvis/fetch-benchmark-name-data/', window.location.origin);
    url.searchParams.append('comparisonMode', compMode);
    url.searchParams.append('compareTargets', compTar1Val);
    url.searchParams.append('compareTargets', compTar2Val);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("bm name data:", data);
            data.forEach(optionText => {
                const option = new Option(optionText, optionText);
                bmNameSelectorElement.add(option);
            });
        });
}