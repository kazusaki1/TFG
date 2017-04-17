var module = angular.module('myIonicApp.controllers');

module.controller('MapCtrl',function($scope,$http,$ionicPopup,ApiEndpoint,$cordovaGeolocation){

var infoWindowClose = false;

  function maps(){

    var options = {timeout: 10000, enableHighAccuracy: true};
    
    //$cordovaGeolocation.getCurrentPosition(options).then(function(position){ // COMENTAR PARA PROBAR EN PC
   
     // var latLng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude); // COMENTAR PARA PROBAR EN PC
     
      var mapOptions = {
       // center: latLng, // COMENTAR PARA PROBAR EN PC
        center: {lat: 41.411321, lng: 2.175568}, // COMENTAR PARA PROBAR EN MOVIL
        zoom: 15,
        mapTypeId: google.maps.MapTypeId.ROADMAP
      };
   
      $scope.map = new google.maps.Map(document.getElementById("map"), mapOptions);

      var marker = [];

      google.maps.event.addListenerOnce($scope.map, 'idle', function(){

          for (var i = 0; i < $scope.eventos.length; i++) { 

              var evento = $scope.eventos[i];

              var markerPos = new google.maps.LatLng(evento.coorX, evento.coorY);
              marker[i] = new google.maps.Marker({
                  map: $scope.map,
                  animation: google.maps.Animation.DROP,
                  position: markerPos
              });      

             
              addInfoWindow(marker[i], evento);
          }

        });
      
    // INI COMENTAR PARA PROBAR EN PC
    /*}, function(error){
      console.log("Could not get location");
    });*/
    // FIN
  }



  function addInfoWindow(marker, message) {




      var infoWindow = new google.maps.InfoWindow();   

      infoWindow.setContent('<p>Event Name: ' + message.event_name + '</p>' +
      '<p>Description: ' + message.event_description + '</p>' +
      '<p>Reward: ' + message.reward + '</p>' +
      '<button onclick="location.href=\'#/app/evento/'+message.id+'\';">Click me</button>'
      );


      google.maps.event.addListener(marker,'click', function () {

          if(infoWindowClose){
            infoWindowClose.close();
          }

          infoWindowClose = infoWindow
          infoWindow.open($scope.map, marker);
                
      });
      
  }


  $scope.header = "Eventos disponibles";
  $scope.eventos = [];
  $http({
    method: 'GET',
    url: ApiEndpoint.url+ 'lista/',
  }).then(function successCallback(response) {
      $scope.eventos = [];
      for(var r in response.data) {
        var evento = response.data[r];
        $scope.eventos.push(evento);       
      }
      maps();

  }, function errorCallback(response) {
      console.log("ERROR");
  }); 

})