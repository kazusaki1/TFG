var module = angular.module('myIonicApp.controllers');

module.controller('RegisterCtrl',function($scope,$http,$ionicPopup,ApiEndpoint,$state,$ionicSideMenuDelegate){
	
	$ionicSideMenuDelegate.canDragContent(false)

	$scope.data = {};
	$scope.register = function() {

		var data = { confirmPassword : $scope.data.confirmPassword, username : $scope.data.username, email : $scope.data.email, password : $scope.data.password};
		var success = false;
		
		$http({
			method:'POST',
			url: ApiEndpoint.url+'register/', 
			data: data,
			headers: {
		      'Content-Type': 'application/json; charset=UTF-8',
		    }

		}).then(function successCallback(response) {
			success = response.data

			if(success == "true")
	            $state.go('app.login');
	        else{
				var alertPopup = $ionicPopup.alert({
			      title: '<u>Register error</u>',
			      template: 'Try again.'
			    })
	        }

		}, function errorCallback(response) {
			console.log("LOGIN ERROR");
		}) 

      
    }

})
