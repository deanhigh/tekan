'use strict';

var techAnalysisApplication = angular.module('techAnalysisApplication',
    [ 'ngRoute', 'symbolsAdmin', 'timeSeries' ]);

techAnalysisApplication.
config(function($logProvider){
    $logProvider.debugEnabled(true);
});