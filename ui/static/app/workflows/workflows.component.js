'use strict';

angular.module('symbolsAdmin').factory('Workflow',
    function ($resource) {
        return $resource('/api/admin/workflows/:workflow', {}, {
            save: {method: 'POST', isArray: true},
            delete: {method: 'DELETE', isArray: true}
        });
    });

angular.module('workflows').component('workflows', {
    templateUrl: 'app/workflows/workflows.template.html',
    controller: function WorkflowsController($scope, Workflow, selectedWorkflow) {
        Workflow.query(function (data) {
            $scope.workflows = data;
        });

        this.addWorkflow = function (wf) {
            this.workflow = new Workflow();

            this.workflow.name = wf.name;
            Workflow.save($scope.workflow, function (response) {
                $scope.workflow.name = "";
                $scope.workflows = response
            });
        };

        this.loadWorkflow = function (name) {
            selectedWorkflow.set(name);
        };

        this.deleteWorkflow = function (name) {
            console.log(name);
            this.workflow = new Workflow();
            this.workflow.name = name;
            Workflow.delete(this.workflow, function (response) {
                $scope.workflows = response
            });
        };
    }
});
