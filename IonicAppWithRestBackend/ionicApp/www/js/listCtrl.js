var module = angular.module('myIonicApp.controllers');

module.controller('ListCtrl',function($scope,$http,$ionicPopup,$state,ApiEndpoint,$cordovaGeolocation, Token, $localstorage, ionicDatePicker){

  $scope.$on('$ionicView.enter', function() {
    Token.isToken()
    
  })
  $scope.currentDate = new Date();

  $scope.lista = [];
  $http({
    method: 'POST',
    url: ApiEndpoint.url+ 'lista/',
    data: $localstorage.get('name')
  }).then(function successCallback(response) {
      $scope.lista = [];
      var ahora = new Date()
      for(var r in response.data) {
        var evento = response.data[r];
        fechaE = new Date(evento.exp_date.slice(0,10));
        if (fechaE > ahora){
          $scope.lista.push(evento); 
        }   
      };

  }, function errorCallback(response) {
      console.log("ERROR Lista");
  }); 

    $http({
        method: 'POST',
        url: ApiEndpoint.url+ 'provincias/',
        data: {'name' : $localstorage.get('name')}
      }).then(function successCallback(response) {
          $scope.listOfOptions2 = [];
          for(var r in response.data) {

            var provincia = response.data[r];
            $scope.listOfOptions2.push(provincia);       
          };
          /*console.log(response.data)*/
          console.log($scope.listOfOptions2)
      }, function errorCallback(response) {
          console.log("ERROR Provincia");
      });

  

  /*$scope.listOfOptions = ['Todos los eventos', 'Localidad', 'Fecha'];*/
  $scope.listOfOptions = ['Todos los eventos', 'Localidad'];
  $scope.selectedItem = 'Todos los eventos'

  $scope.selectedItemChanged = function(selectedItem){
    $scope.selectedItem = selectedItem

    if (selectedItem == 'Todos los eventos'){
      type = 't'
      $scope.tipo = 't'
      $scope.lista = [];
      $http({
        method: 'POST',
        url: ApiEndpoint.url+ 'lista/',
        data: $localstorage.get('name')
      }).then(function successCallback(response) {
          var ahora = new Date()
          $scope.lista = [];
          for(var r in response.data) {
            var evento = response.data[r];

            fechaE = new Date(evento.exp_date.slice(0,10));
            if (fechaE > ahora){
              $scope.lista.push(evento); 
            }else{
            }      
          };

      }, function errorCallback(response) {
          console.log("ERROR");
      });
    }else if (selectedItem == 'Localidad'){
      type = 'l'
      $scope.tipo = 'l'
    }else if (selectedItem == 'Fecha'){
      type = 'f'
      $scope.tipo = 'f'
    }

   
  }

  $scope.selectedItemChanged2 = function(selectedItem){
    console.log($scope.listOfOptions2)
    $scope.selectedItem2 = selectedItem
    $scope.lista = []
    tipo = $scope.tipo
    info = $scope.selectedItem2
    $http({
      method: 'POST',
      url: ApiEndpoint.url+ 'listaFiltrada/',
      data: {'username' : $localstorage.get('name'), 'type' : tipo, 'info' : info}
    }).then(function successCallback(response) {
      var ahora = new Date()
        $scope.lista = [];
        for(var r in response.data) {
          var eventoPro = response.data[r];
          fechaE = new Date(eventoPro.exp_date.slice(0,10));
            if (fechaE > ahora){
              $scope.lista.push(eventoPro); 
            }    
        };
    }, function errorCallback(response) {
        console.log("ERROR Filtro");
    });
  }

})