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
    $scope.buttons['deluge_btn'] = '/deluge_status';
    $scope.buttons['syncthing_btn'] = '/syncthing_status';
    $scope.buttons['display_up_btn'] = '/display_up';
    $scope.buttons['reboot_btn'] = '/reboot';

    // A dict of all supported buttons:
    // Order:
    // key  = ID of the button
    // value= port to redirect to for local links
    $scope.internal_redirects = {};
    $scope.internal_redirects['deluge_btn'] = '6788';
    $scope.internal_redirects['syncthing_btn'] = '8384';

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
                        // Redirects to a new tab with respective page.
                        if (event.target.id in $scope.internal_redirects)
                            window.open("//" + window.location.hostname + ":" +
                                $scope.internal_redirects[event.target.id]);
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
