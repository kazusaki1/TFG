var module = angular.module('myIonicApp.controllers');

module.controller('EventCtrl',function($scope,$http,$ionicPopup,ApiEndpoint){
    $scope.header = "Eventos disponibles";
    $scope.eventos = [];
    $http({
      method: 'GET',
      url: ApiEndpoint.url+ 'eventos/',
    }).then(function successCallback(response) {
        $scope.eventos = [];
        for(var r in response.data) {
          var evento = response.data[r];
          $scope.eventos.push(evento);
        }
        console.log($scope.eventos);
    }, function errorCallback(response) {
        console.log("ERROR");
    });    
})