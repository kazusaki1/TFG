var module = angular.module('myIonicApp.controllers');

module.controller('LoginCtrl',function($scope,$http,$ionicPopup,ApiEndpoint,$state,$localstorage,$ionicSideMenuDelegate){
	
	$ionicSideMenuDelegate.canDragContent(false)

	$scope.data = {};
	$scope.login = function() {

		var data = {username : $scope.data.username, password : $scope.data.password};
		var success = false;
		$http({
			method:'POST',
			url: ApiEndpoint.url+'login/', 
			data: data,
			headers: {
		      'Content-Type': 'application/json; charset=UTF-8',
		    }

		}).then(function successCallback(response) {
			success = response.data

			if(success[0].access == "true"){
				$localstorage.set('name', $scope.data.username);
				$localstorage.set('token', success[0].token);
				//$localstorage.clear('name');
				//$localstorage.clear('token');
	            $state.go('app.home');
			}else{
				var alertPopup = $ionicPopup.alert({
			      title: '<u>Login error</u>',
			      template: 'The user name or password is incorrect.'
			    })
	        }

		}, function errorCallback(response) {
			console.log("LOGIN ERROR");
		}) 

      
    }

})
