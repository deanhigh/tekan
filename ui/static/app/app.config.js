/**
 * Created by dean.high on 15/10/2016.
 */

angular.
module('techAnalysisApplication').
config(['$locationProvider', '$routeProvider',
    function config($locationProvider, $routeProvider) {
        $locationProvider.hashPrefix('!');
        $routeProvider.
        when('/symbols', {
            template:   '<symbols-admin></symbols-admin>'
        }).
        when('/ts', {
            template: '<ts-viewer></ts-viewer>'
        }).
        otherwise('/symbols');
    }
]);