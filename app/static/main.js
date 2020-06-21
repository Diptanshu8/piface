(function () {

  angular.module('PiFaceApp', [])

  .controller('PiFaceController', ['$scope', '$log', '$http',
    function($scope, $log, $http) {
    // A dict of all supported buttons:
        // Order:
        // key  = ID of the button
        // value= callback to the server
    $scope.buttons = {};
    $scope.buttons['ip_addr_btn'] = '/get_ip_addr';
    $scope.buttons['mnt_stat_btn'] = '/nas_mount_status';
    $scope.buttons['delg_stat_btn'] = '/deluge_status';
    $scope.buttons['delgweb_stat_btn'] = '/delugeweb_status';
    $scope.buttons['retropie_launch_btn'] = '/launch_retropie';
    $scope.buttons['display_up_btn'] = '/display_up';
    $scope.buttons['reboot_btn'] = '/reboot';
    
        $scope.btn_click = function(event) {
            var button = angular.element(document.getElementById(event.target.id));
            // Check if the button ID is added to $scope.buttons for callback.
            if (!(event.target.id in $scope.buttons))
                alert(event.target.id + " is invalid ID.");
            else {
                // Check if the button is already pressed and status is being shown.
                if (button.hasClass("btn-primary")) {
                    var old = button.text() + ": ";
                    button.removeClass("btn-primary");
                    $http.get($scope.buttons[event.target.id]).
                            success(function(data) {
                              $log.log(data);
                              button.text(old+data);
                              button.addClass("btn-success");
                            }).
                            error(function(error) {
                                $log.log(error);
                                button.text(old+error);
                                button.addClass("btn-danger");
                            });
                }
                else 
                    alert("Status already being shown. Reload and click again!");
            }
		};
    }
  ]);
}());
