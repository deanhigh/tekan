'use strict';

angular.
module('techAnalysisApplication').
config(['$locationProvider', '$routeProvider',
    function config($locationProvider, $routeProvider) {
        $locationProvider.hashPrefix('!');
        $routeProvider.
        when('/time-series', {
            template: '<time-series></time-series>'
        }).
        when('/symbols', {
            template: '<symbols-admin></symbols-admin>'
        }).
        when('/workflows', {
            template: '<workflows></workflows>'
        }).
        otherwise('/symbols');
    }
]);