(function() {
    // Scroll Variables (tweakable)
    var defaultOptions = {
        frameRate: 150,
        animationTime: 400,
        stepSize: 120,
        pulseAlgorithm: true,
        pulseScale: 8,
        pulseNormalize: 1,
        accelerationDelta: 20,
        accelerationMax: 1,
        keyboardSupport: true,
        arrowScroll: 50,
        touchpadSupport: true,
        fixedBackground: true,
        excluded: ""
    };

    var options = defaultOptions;
    var root = document.documentElement;
    var activeElement;
    var initDone = false;

    // Define the refresh function
    function refresh() {
        var body = document.body;
        var html = document.documentElement;

        var windowHeight = window.innerHeight;
        var scrollHeight = body.scrollHeight;

        // Adjust height if necessary
        if (scrollHeight > windowHeight && (body.offsetHeight <= windowHeight || html.offsetHeight <= windowHeight)) {
            html.style.height = 'auto';
        }
    }

    // Initialize function
    function init() {
        if (!document.body) return;

        var body = document.body;
        var html = document.documentElement;
        var windowHeight = window.innerHeight;
        var scrollHeight = body.scrollHeight;

        root = (document.compatMode.indexOf('CSS') >= 0) ? html : body;
        activeElement = body;

        initDone = true;

        // Call refresh to adjust styles after initialization
        refresh(); // Ensure refresh is called after defining it

        // Additional logic can be added here...
    }

    // Call init on load
    window.onload = init;

    // Add other event listeners and functions as needed...
})();
