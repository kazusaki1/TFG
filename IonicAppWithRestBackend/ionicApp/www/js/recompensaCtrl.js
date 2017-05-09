var module = angular.module('myIonicApp.controllers');

module.controller('RecompensaCtrl', function($scope, $http, $ionicModal, $timeout, $localstorage, ApiEndpoint, ionicMaterialInk) {

	ionicMaterialInk.displayEffect();

	$scope.eventosDeUsuario = [];
	var data = {name : $localstorage.get('name')}
	console.log(data);    
  	$http({
    	method: 'POST',
    	data: data,
    	url: ApiEndpoint.url+ 'eventosDeUsuario/',
    	headers: {
		      'Content-Type': 'application/json; charset=UTF-8',
		}
  	}).then(function successCallback(response) {    
      	$scope.eventosDeUsuario = [];
      	for(var r in response.data) {
          var evento = response.data[r];
          $scope.eventosDeUsuario.push(evento);   
        };


  }, function errorCallback(response) {

      console.log("ERROR recompensas");
  });
})
