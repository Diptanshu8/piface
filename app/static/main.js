(function () {

  angular.module('PiFaceApp', [])

  .controller('PiFaceController', ['$scope', '$log', '$http',
    function($scope, $log, $http) {
    $scope.buttons_list = [
        {
            'id'      : 'IP Address',
            'route'     : '/get_ip_addr',
            'redirect'  : "",
            'show'      : true,
        },
        {
            'id'      : 'Mount Status',
            'route'     : '/nas_mount_status',
            'redirect'  : "",
            'show'      : true,
        },
        {
            'id'      : 'Deluge Status',
            'route'     : '/deluge_status',
            'redirect'  : '6788',
            'show'      : true,
        },
        {
            'id'      : 'Syncthing Status',
            'route'     : '/syncthing_status',
            'redirect'  : '8384',
            'show'      : true,
        },
        {
            'id'      : 'Launch Retropie',
            'route'     : '/launch_retropie',
            'redirect'  : "",
            'show'      : true,
        },
        {
            'id'      : 'Magic Mirror Start',
            'route'     : '/magicmirror_start',
            'redirect'  : '8080',
            'show'      : true,
        },
        {
            'id'      : 'Magic Mirror Stop',
            'route'     : '/magicmirror_stop',
            'redirect'  : "",
            'show'      : true,
        },
        {
            'id'      : 'Reboot Raspi',
            'route'     : '/reboot',
            'redirect'  : '',
            'show'      : true,
        },
    ];

    $scope.button_click = function(src_id) {
        var button = angular.element(document.getElementById(src_id));
        // Check if the ID from ng-click matches the IDs present in the list of buttons.
        // Either of too many buttons with same ID or no buttons with matching ID is a problem.
        // TODO: Handle the errors in seperate alerts.
        var buttons = $scope.buttons_list.filter(function(obj) {
                    return obj.id == src_id;});
        if (buttons.length != 1)
            alert(src_id + " is invalid button ID.");
        else {
            $log.log(src_id);
            var b = buttons[0];
            if (button.hasClass("btn-primary")) {
                var old = button.text() + ": ";
                button.removeClass("btn-primary");
                // TODO: add timeout and remove just one time click feature via btn-primary class check.
                $http.get(b.route).
                    success(function(data) {
                        $log.log(data);
                        button.text(old+data);
                        button.addClass("btn-success");
                        // Redirects to a new tab with respective page.
                        if (b.redirect!="") {
                            window.open("//" + window.location.hostname + ":" +b.redirect);
                        }
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
