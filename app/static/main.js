(function () {

  angular.module('PiFaceApp', [])

  .controller('PiFaceController', ['$scope', '$log', '$http',
    function($scope, $log, $http) {
	$scope.ip_show = false;
    $scope.ip_addr = "X";

        $scope.btn_click = function(btn_id) {
            $log.log(btn_id)
			if (btn_id == 'ip_addr_btn') {
                if ($scope.ip_show) {
                    alert("IP already being shown!");
                }
				$http.get('/get_ip_addr').
                    success(function(data) {
					  $scope.ip_addr=data;
                      $scope.ip_show = true;
					  $log.log(data);
					}).
                    error(function(error) {
                        $log.log(error);
                    });
            }
		};
    }
  ]);
}());
