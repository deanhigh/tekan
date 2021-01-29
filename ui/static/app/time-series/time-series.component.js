'use strict';

angular.
module('timeSeries').
component('timeSeries', {
    templateUrl: 'app/time-series/time-series.template.html',
    controller: function TimeSeriesController($scope) {
        console.log($scope);
        this.loadTimeSeries = function () {
            console.log($scope);
        };
    }
});
