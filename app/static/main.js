(function () {

  angular.module('PiFaceApp', [])

  .controller('PiFaceController', ['$scope', '$log', '$http',
    function($scope, $log, $http) {
    // A dict of all supported features:
        // Order:
        // key = ID of the button
        // Value = "Text appearing on page", "corresponding callback to server to process the request",
        //          "status of the ng-disabled variable", "output to be displayed"
    $scope.features = {};
    $scope.features['ip_addr_btn'] = ['IP Address','/get_ip_addr', false, ''];
    $scope.features['mnt_stat_btn'] = ['NAS mount status','/nas_mount_status', false, ''];
    $scope.features['delg_stat_btn'] = ['Deluge Daemon status','/deluge_status', false, ''];
    $scope.features['delgweb_stat_btn'] = ['Deluge Web status','/delugeweb_status', false, ''];
    $scope.features['retropie_launch_btn'] = ['Launch Retropie','/launch_retropie', false, ''];
    $scope.features['display_up_btn'] = ['Power Display Up','/display_up', false, ''];
    $scope.features['reboot_btn'] = ['Reboot Raspi','/reboot', false, ''];
	$scope.present = [];
    
        $scope.btn_click = function(event) {
            var i;
            var found = false;
            var btn_id = event.target.id;
            var button = angular.element(document.getElementById(event.target.id));

            // Check if the feature is being already displayed and raise an 
            // alert in that case.
            // Else find the feature to be displayed from btn_id, process
            // and display it and add it to the present list.
            for (i = 0; i < $scope.present.length; i++){
                if ($scope.present[i] == $scope.features[btn_id]) {
                    found = true;
                    break;
                }
            } 
            if (found) 
                 alert($scope.present[i][0] + " being shown!");
            else {
                for (var key in $scope.features) {
                    if (btn_id == key)
                            $scope.present.push($scope.features[key]);
                }
                //$log.log($scope.present);
                var j = $scope.present.length-1
                $http.get($scope.present[j][1]).
                        success(function(data) {
                          $scope.present[j][3]=data;
                          $scope.present[j][2] = true;
                          $log.log(data);
                          button.removeClass("btn-primary");
                          button.addClass("btn-success");
                        }).
                        error(function(error) {
                            $scope.present[j][3]=error;
                            $scope.present[j][2] = true;
                            button.removeClass("btn-primary");
                            button.addClass("btn-danger");
                            $log.log(error);
                        });
                }
		};
    }
  ]);
}());
