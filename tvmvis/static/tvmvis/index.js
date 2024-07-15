//Selector Initialization
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.comparison-mode-selector').forEach(function (selectorElement) {
        setSelector(selectorElement, ["byRun", "byDevice"]);
    })

    document.querySelectorAll('.parameter-selector').forEach(function (selectorElement) {
        const url = new URL('/tvmvis/fetch-param-types-data/', window.location.origin);
        fetch(url)
            .then(response => response.json())
            .then(data => {
                console.log("param types data:")
                console.log(data)
                data.forEach(function (optionText) {
                    const option = new Option(optionText, optionText);
                    selectorElement.add(option)
                })

            })
    })

    document.querySelectorAll('.comparison-mode-selector').forEach(function (selectorElement) {
        const groupLayout = selectorElement.closest('.title-sel-group');
        let targetSelectorElement = groupLayout.querySelector('.comparison-target-selector');
        updateTargetSelector(targetSelectorElement, selectorElement.value)

        let targetSelectorElementCompare = groupLayout.querySelector('.comparison-target-selector-compared');
        updateTargetSelector(targetSelectorElementCompare, selectorElement.value)
    })

});


document.addEventListener('DOMContentLoaded', function () {

    //Update comparison-target-selector, comparison-target-selector-compared
    //according to comp mode value when it changes
    document.querySelectorAll('.comparison-mode-selector').forEach(function (selectorElement) {
        const groupLayout = selectorElement.closest('.title-sel-group');
        selectorElement.addEventListener('change', function () {
            let targetSelectorElement = groupLayout.querySelector('.comparison-target-selector');
            updateTargetSelector(targetSelectorElement, selectorElement.value)

            let targetSelectorElementCompare = groupLayout.querySelector('.comparison-target-selector-compared');
            updateTargetSelector(targetSelectorElementCompare, selectorElement.value)
        })
    })

    //Update benchmark-name-selector according to comp target values
    document.querySelectorAll('.comparison-target-selector, .comparison-target-selector-compared').forEach(function (selectorElement) {
        const groupLayout = selectorElement.closest('.title-sel-group');

        let bmNameSelectorElement = groupLayout.querySelector('.benchmark-name-selector');
        let targetSelectorElement = groupLayout.querySelector('.comparison-target-selector');
        let targetSelectorElementCompare = groupLayout.querySelector('.comparison-target-selector-compared');

        let compMode = groupLayout.querySelector('.comparison-mode-selector').value;

        selectorElement.addEventListener('change', function () {
            updateBenchmarkNameSelector(bmNameSelectorElement, compMode,
                targetSelectorElement.value, targetSelectorElementCompare.value)
        })
    })

    document.querySelectorAll('.generate-button').forEach(function (ButtonElement) {
        ButtonElement.addEventListener('click', function () {
            console.log("Start Generate")
            const groupLayout = ButtonElement.closest('.title-sel-group');
            let bmName = groupLayout.querySelector('.benchmark-name-selector').value;
            let target = groupLayout.querySelector('.comparison-target-selector').value;
            let targetCompared = groupLayout.querySelector('.comparison-target-selector-compared').value;
            let compMode = groupLayout.querySelector('.comparison-mode-selector').value;
            let paramType = groupLayout.querySelector('.parameter-selector').value;
            let runIds = [];
            let deviceNames = [];
            if (compMode == "byRun") {
                runIds.push(target);
                runIds.push(targetCompared);
            } else {
                deviceNames.push(target);
                deviceNames.push(targetCompared);
            }
            updateTable(ButtonElement, compMode, paramType, runIds, deviceNames, bmName)
        })

    })

});


function setSelector(selectElement, options) {
    // Add option for <select>
    options.forEach(function (optionText) {
        var option = new Option(optionText, optionText);
        selectElement.add(option);
    });

}

function updateTargetSelector(targetSelectorElement, comparisonMode) {

    //Clean previous options
    while (targetSelectorElement.options.length > 0) {
        targetSelectorElement.remove(0);
    }

    //Fetch comparison option data and add into selector
    const url = new URL('/tvmvis/fetch-relative-mode-data/', window.location.origin);
    url.searchParams.append('comparisonMode', comparisonMode);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("relative mode data:")
            console.log(data)
            data.forEach(function (optionText) {
                const option = new Option(optionText, optionText);
                targetSelectorElement.add(option)
            })

        })

}

function updateBenchmarkNameSelector(bmNameSelectorElement, compMode, compTar1Val, compTar2Val) {
    //Clean previous options
    while (bmNameSelectorElement.options.length > 0) {
        bmNameSelectorElement.remove(0);
    }
    //Fetch bm name option data and add into selector
    const url = new URL('/tvmvis/fetch-benchmark-name-data/', window.location.origin);
    url.searchParams.append('comparisonMode', compMode);
    url.searchParams.append('compareTargets', compTar1Val);
    url.searchParams.append('compareTargets', compTar2Val);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("bm name data:")
            console.log(data)
            data.forEach(function (optionText) {
                const option = new Option(optionText, optionText);
                bmNameSelectorElement.add(option)
            })

        })
}