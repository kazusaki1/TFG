var module = angular.module('myIonicApp.controllers');

module.controller('RecompensaCtrl', function($scope, $http, $ionicModal, $timeout, $localstorage, ApiEndpoint, ionicMaterialInk) {

	ionicMaterialInk.displayEffect();
  $scope.username = $localstorage.get('name')
	$scope.eventosDeUsuario = [];
	var data = {name : $localstorage.get('name')}  
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
          evento['mostrar'] = "Mostrar recompensa"
          evento['resultado'] = "**************"
          $scope.eventosDeUsuario.push(evento);   
        };


  }, function errorCallback(response) {

      console.log("ERROR recompensas");
  });

  $scope.mostrar = function(evento){
    if(evento['mostrar'] == "Mostrar recompensa"){
      evento['mostrar'] = "Ocultar recompensa"
      evento['resultado'] = evento['key']

    }else{
      evento['mostrar'] = "Mostrar recompensa"
      evento['resultado'] = "**************"
    }
  }

})
