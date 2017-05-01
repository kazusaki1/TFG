var module = angular.module('myIonicApp.controllers');

module.controller('ImageCtrl', function($scope, ImageService) {
 
 
  $scope.addMedia = function(brand,event_id) {
	
	  ImageService.takePhoto(brand,event_id).then(function() {

    });
  }

  
});
