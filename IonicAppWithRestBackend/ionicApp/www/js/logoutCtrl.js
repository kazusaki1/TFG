var module = angular.module('myIonicApp.controllers');

module.controller('LogoutCtrl',function($state,$localstorage,$scope,$ionicHistory){

	$scope.logout = function() {
		$ionicHistory.clearCache();
		$ionicHistory.clearHistory();
		$localstorage.clear('name');
		$localstorage.clear('token');
		$state.go('app.login');
	}

})
