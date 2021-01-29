'use strict';

angular.module('symbolsAdmin').factory('Symbol',
    function ($resource) {
        return $resource('/api/admin/symbols/:ticker', {}, {
            save: {method: 'POST', isArray: true},
            delete: {method: 'DELETE', isArray: true}
        });
    });

angular.module('symbolsAdmin').factory('SymbolSync',
    function ($resource) {
        return $resource('/api/admin/symbols-sync');
    });

angular.module('symbolsAdmin').component('symbolsAdmin', {
    templateUrl: 'app/symbols-admin/symbols-admin.template.html',
    controller: function SymbolsListController($scope, Symbol, SymbolSync) {
        this.symbols = Symbol.query(function (data) {
            $scope.symbols = data;
        });

        this.addSymbol = function () {
            $scope.symbol = new Symbol();
            $scope.symbol.ticker = $scope.form.ticker;
            Symbol.save($scope.symbol, function (response) {
                $scope.form.ticker = "";
                $scope.symbols = response
            });
        };

        $scope.selectedTicker = null;
        $scope.setSelected = function (selectedTicker) {
            $scope.selectedTicker = selectedTicker;
        };

        this.deleteSelected = function (ticker) {
            $scope.symbol = new Symbol();
            $scope.symbol.ticker = ticker;
            Symbol.delete($scope.symbol, function (response) {
                $scope.symbols = response
            });
        };

        this.syncAll = function() {
            // var service = $resource('/api/admin/symbols-sync');
            // service.post();
            $scope.sync = SymbolSync();
            SymbolSync.save($scope.sync);
        };
    }
});