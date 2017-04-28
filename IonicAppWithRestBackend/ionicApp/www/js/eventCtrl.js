var module = angular.module('myIonicApp.controllers');

module.controller('EventCtrl',function($scope,$http,$ionicPopup,ApiEndpoint,$cordovaGeolocation,$stateParams, Token){

  $scope.$on('$ionicView.enter', function() {
    Token.isToken()
    
  })

  $scope.header = "Informacion evento";
  $scope.evento = [];
  $http({
    method: 'GET',
    url: ApiEndpoint.url+ 'evento/' + $stateParams.id +'/',
  }).then(function successCallback(response) {      
      $scope.evento = [];
      for(var r in response.data) {
        var info = response.data[r];
        $scope.evento.push(info);       
      }

  }, function errorCallback(response) {
      console.log("ERROR");
  }); 
})