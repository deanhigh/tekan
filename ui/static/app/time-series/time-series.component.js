'use strict';

angular.module('timeSeries').component('timeSeries', {
    templateUrl: 'app/time-series/time-series.template.html',
    controller: function TimeSeriesController($scope, $http, timeSeriesConfig) {
        $scope.ticker = timeSeriesConfig.get();

        console.log($scope.ticker);

        $http.get("/api/time-series/".concat($scope.ticker))
            .success(function (response) {
                new Dygraph(document.getElementById("primaryTimeSeriesGraph"), response,
                    {
                        title: $scope.ticker,
                        labelsDivStyles: { 'textAlign': 'right' },
                        showRangeSelector: true
                    });
            });
    }
});
