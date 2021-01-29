'use strict';

var techAnalysisApplication = angular.module('techAnalysisApplication',
    [ 'ngRoute', 'symbolsAdmin', 'timeSeries', 'workflows', 'workflowBuilder' ]);

angular.module('techAnalysisApplication').factory('timeSeriesConfig', function() {
    var config = {};
    function set(data) {
        config = data;
    }
    function get() {
        return config;
    }
    return {
        set: set,
        get: get
    }
});