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
      console.log(ahora)
      for(var r in response.data) {

        console.log(response.data[r])
        var evento = response.data[r];
        fechaE = new Date(evento.exp_date.slice(0,10));
        if (fechaE > ahora){
          console.log("evento mas grande")
          $scope.lista.push(evento); 
        }else{
          console.log("ahora es mas grande")
        }
        console.log(fechaE)
              
      };

  }, function errorCallback(response) {
      console.log("ERROR");
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
          console.log("ERROR");
      });

  

  $scope.listOfOptions = ['Todos los eventos', 'Localidad', 'Fecha'];
  $scope.selectedItem = 'Todos los eventos'

  $scope.selectedItemChanged = function(selectedItem){
    /*console.log($scope.listOfOptions)*/
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
            /*console.log(response.data[r])*/
            var evento = response.data[r];

            fechaE = new Date(evento.exp_date.slice(0,10));
            if (fechaE > ahora){
              console.log("evento mas grande")
              $scope.lista.push(evento); 
            }else{
            console.log("ahora es mas grande")
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
    console.log($scope.tipo)
    console.log($scope.selectedItem2)
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
          /*console.log(response.data[r])*/
          var eventoPro = response.data[r];
          fechaE = new Date(eventoPro.exp_date.slice(0,10));
            if (fechaE > ahora){
              console.log("evento mas grande")
              $scope.lista.push(eventoPro); 
            }else{
            console.log("ahora es mas grande")
            }  
          /*console.log($scope.selectedItem2)*/     
        };
    }, function errorCallback(response) {
        console.log("ERROR");
    });
  }

})