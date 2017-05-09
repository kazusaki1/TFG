var module = angular.module('myIonicApp.controllers');

module.controller('PerfilCtrl', function($scope, $http, $ionicPopup, $state, $ionicModal, $timeout, $localstorage, ApiEndpoint, ionicMaterialInk) {

	ionicMaterialInk.displayEffect();

	$scope.userInfo = [];
	var data = {name : $localstorage.get('name')}
	console.log(data);    
  	$http({
    	method: 'POST',
    	data: data,
    	url: ApiEndpoint.url+ 'perfilPropio/',
    	headers: {
		      'Content-Type': 'application/json; charset=UTF-8',
		}
  	}).then(function successCallback(response) {    
      	
      	for(var r in response.data) {
          var datos = response.data[r];
          $scope.userInfo.push(datos);   
        };


  }, function errorCallback(response) {

      console.log("ERROR carga email");
  });


	$scope.data = {};
	$scope.actualizar = function() {

		var data = {name : $localstorage.get('name'), email : $scope.data.email, password : $scope.data.password, confirmPassword : $scope.data.confirmPassword};
		var success = false;
		$http({
			method:'POST',
			url: ApiEndpoint.url+'perfilActualizado/', 
			data: data,
			headers: {
		      'Content-Type': 'application/json; charset=UTF-8',
		    }

		}).then(function successCallback(response) {
			success = response.data

			if(success == "true"){
				var alertPopup = $ionicPopup.alert({
			      title: '<u>Datos modificados con éxito</u>',
			      template: 'Pulsa Ok para aparecer en la Home'
			    })
	            $state.go('app.home');
			}
				
	        else{
				var alertPopup = $ionicPopup.alert({
			      title: '<u>Error al modificar datos</u>',
			      template: 'Try again.'
			    })
	        }

			

		}, function errorCallback(response) {
			console.log("ERROR actualizacion");
		}) 

      
    }
})
