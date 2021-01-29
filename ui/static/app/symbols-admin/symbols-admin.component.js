'use strict';

angular.
module('symbolsAdmin').
factory('Symbol',
    function($resource) {
        return $resource('/api/admin/symbols', {}, {
            save: {method:'POST', isArray:true}
        });
    });

angular.
module('symbolsAdmin').component('symbolsAdmin', {
    templateUrl: 'app/symbols-admin/symbols-admin.template.html',
    controller: function SymbolsListController($scope, Symbol) {
        this.symbols = Symbol.query(function (data) {
            $scope.symbols = data;
        });
        
        this.addSymbol = function(e) {
            $scope.symbol = new Symbol();
            $scope.symbol.ticker = $scope.form.ticker;
            Symbol.save($scope.symbol, function(response) {
                console.log(response);
                $scope.symbols = response
            });
        };
    }
});