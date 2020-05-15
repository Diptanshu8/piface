(function () {

  angular.module('PiFaceApp', [])

  .controller('PiFaceController', ['$scope', '$log',
    function($scope, $log) {
        $scope.homepage = function() {
            $log.log("Inside controller function");
			};
    }
  ]);
}());
