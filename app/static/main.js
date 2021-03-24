(function () {

  angular.module('PiFaceApp', [])

  .controller('PiFaceController', ['$scope', '$log', '$http', '$timeout',
    function($scope, $log, $http, $timeout) {
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
        // buttons is a list of all the buttons in buttons_list which match the ID of event source button.
        var buttons = $scope.buttons_list.filter(function(obj) {
                    return obj.id == src_id;});
        if (buttons.length == 0)
            alert(src_id + " is invalid button ID.");
        else if (buttons.length > 1) {
            $log.log(buttons);
            alert("Multiple buttons have same ID as the event source button. Please check the console log.");
        }
        else {
            // Ideally buttons should contain just one element matching the ID of event source button.
            $log.log(src_id);
            var b = buttons[0];
            var old = button.text();
            button.removeClass("btn-primary");
            $http.get(b.route).
                success(function(data) {
                    $log.log(data);
                    button.text(old+":"+data);
                    button.addClass("btn-success");
                    // Redirects to a new tab with respective page.
                    if (b.redirect!="")
                        window.open("//" + window.location.hostname + ":" +b.redirect);
                }).
                error(function(error) {
                    $log.log(error);
                    button.text(old+error);
                    button.addClass("btn-danger");
                });
                $timeout(function(){
                    button.text(old);
                    if (button.hasClass("btn-success"))
                        button.removeClass("btn-success");
                    if (button.hasClass("btn-danger"))
                        button.removeClass("btn-danger");
                    button.addClass("btn-primary");
                }, 3000);
        }
    };
    }
  ]);
}());

// Function to load the sidebar depending on the device width.
$(function(){
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });

    $(window).resize(function(e) {
      if($(window).width()<=768){
        $("#wrapper").removeClass("toggled");
      }else{
        $("#wrapper").addClass("toggled");
      }
    });
});
