var module = angular.module('myIonicApp.controllers');

module.controller('ImageCtrl', function($scope, ImageService) {
 
 
  $scope.addMedia = function(brand) {
	
	  ImageService.takePhoto(brand).then(function() {

    });
  }

  
});
