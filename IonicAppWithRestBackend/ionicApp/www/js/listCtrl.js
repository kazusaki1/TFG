var module = angular.module('myIonicApp.controllers');

module.controller('ListCtrl',function($scope,$http,$ionicPopup,ApiEndpoint,$cordovaGeolocation, Token){

$scope.$on('$ionicView.enter', function() {
  Token.isToken()
  
})

$scope.lista = [];
  $http({
    method: 'GET',
    url: ApiEndpoint.url+ 'lista/',
  }).then(function successCallback(response) {
      $scope.lista = [];
      for(var r in response.data) {
        var evento = response.data[r];
        $scope.lista.push(evento);       
      };

  }, function errorCallback(response) {
      console.log("ERROR");
  }); 
})