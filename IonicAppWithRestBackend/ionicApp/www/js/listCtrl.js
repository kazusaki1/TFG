var module = angular.module('myIonicApp.controllers');

module.controller('ListCtrl',function($scope,$http,$ionicPopup,ApiEndpoint,$cordovaGeolocation, Token, $localstorage){

  $scope.$on('$ionicView.enter', function() {
    Token.isToken()
    
  })

  $scope.lista = [];
  $http({
    method: 'POST',
    url: ApiEndpoint.url+ 'lista/',
    data: $localstorage.get('name')
  }).then(function successCallback(response) {
      $scope.lista = [];
      for(var r in response.data) {
        var evento = response.data[r];
        $scope.lista.push(evento);       
      };

  }, function errorCallback(response) {
      console.log("ERROR");
  }); 


  $scope.listOfOptions = ['Todos los eventos', 'Localidad', 'Fecha'];
  $scope.selectedItem = 'Todos los eventos'

  $scope.selectedItemChanged = function(selectedItem){

    $scope.selectedItem = selectedItem

    if (selectedItem == 'Todos los eventos'){
      type = 't'
    }else if (selectedItem == 'Localidad'){
      type = 'l'
    }else if (selectedItem == 'Fecha'){
      type = 'f'
    }

    $http({
      method: 'POST',
      url: ApiEndpoint.url+ 'listaFiltrada/',
      data: {'username' : $localstorage.get('name'), 'type' : type}
    }).then(function successCallback(response) {
        $scope.lista = [];
        for(var r in response.data) {
          var evento = response.data[r];
          $scope.lista.push(evento);       
        };
    }, function errorCallback(response) {
        console.log("ERROR");
    });
  }

})