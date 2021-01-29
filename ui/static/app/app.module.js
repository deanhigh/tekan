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

angular.module('techAnalysisApplication').factory('selectedWorkflow', function() {
    var selected = {};
    function set(data) {
        selected = data;
    }
    function get() {
        return selected;
    }
    return {
        set: set,
        get: get
    }
});