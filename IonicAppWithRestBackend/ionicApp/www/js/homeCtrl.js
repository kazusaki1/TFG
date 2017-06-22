var module = angular.module('myIonicApp.controllers');

module.controller('HomeCtrl',function($scope,$http,$ionicPopup,ApiEndpoint){
    $scope.header = "Where is the pipol";
    $scope.personas = [];
    $http({
      method: 'GET',
      url: ApiEndpoint.url+ 'personas/',
    }).then(function successCallback(response) {
        $scope.personas = [];
        for(var r in response.data) {
          var persona = response.data[r];
          $scope.personas.push(persona);
        }
        console.log($scope.smuglers);
    }, function errorCallback(response) {
        console.log("ERROR");
    });
})



