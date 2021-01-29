'use strict';

// angular.
// module('timeSeries').factory('TimeSeries',
//     function ($resource) {
//         return $resource('/api/time-series/:ticker');
//     });


angular.module('timeSeries').component('timeSeries', {
    templateUrl: 'app/time-series/time-series.template.html',
    controller: function TimeSeriesController($scope, $http) {
        this.loadTimeSeries = function () {
        };

        //console.log(TimeSeries.query());
        $http.get("/api/time-series")
            .success(function (response) {
                new Dygraph(document.getElementById("primaryTimeSeriesGraph"), response);
            });
    }
});
