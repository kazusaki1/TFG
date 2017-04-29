var module = angular.module('myIonicApp.controllers');

module.controller('MapCtrl',function($scope,$http,$ionicPopup,ApiEndpoint,$cordovaGeolocation,$localstorage,Token){

  var timer, timer2
   // Code you want executed every time view is opened
  $scope.$on('$ionicView.enter', function() {
    
    Token.isToken()

    var infoWindowClose = false;
    var latLng = null;
    var options = {timeout: 10000, enableHighAccuracy: true};
    var myImage = '/img/userMaps.png';
    map = new google.maps.Map(document.getElementById("map"));

    // My marker
    var myMarker = new google.maps.Marker({
          map: map,
          //icon: ApiEndpoint.url+"media/34250_GjGILec.png"
          icon: myImage
    }); 

    var markers = [];

    // Get my current position. If ubication is disabled: lat: 41.411321, lng: 2.175568
    $cordovaGeolocation.getCurrentPosition(options).then(function(position){ 
       
      latLng = {lat: position.coords.latitude, lng: position.coords.longitude};
      initMap();
      
    }, function(error){
      console.log("Could not get location");
      latLng = {lat: 41.411321, lng: 2.175568};
      initMap();
      
    });


    function initMap(){

      var mapOptions = {
        center: latLng,
        zoom: 15,
        mapTypeId: google.maps.MapTypeId.ROADMAP
      };

      map.setCenter(latLng);
      map.setZoom(15);
      map.setMapTypeId(google.maps.MapTypeId.ROADMAP);

      getEvents();
           
    }


    timer = setInterval(function(){
          $cordovaGeolocation.getCurrentPosition(options).then(function(position){ 
         
        latLng = {lat: position.coords.latitude, lng: position.coords.longitude};
        }, function(error){
          latLng = {lat: 41.411321, lng: 2.175568};
        });
          myMarker.setPosition(latLng);

    }, 1000);


    timer2 = setInterval(function(){
        getEvents();

    }, 10000);


    function createMarkers(){
      //var image = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
      var eventoImg = '/img/eventoMaps.png';
      var paradaImg = '/img/paradaMaps.png';
      for(var x = 0; x < markers.length; x++){
        if(markers[x] != null)
          markers[x].usado = false;
      }

      
      for(var i = 0; i < $scope.eventos.length; i++){
        var cont = 0
        evento = $scope.eventos[i]


        var existe = false;
        for(var j = 0; j < markers.length; j++){
            if(markers[j] != null && evento.id == markers[j].id){
              existe = true
              markers[j].usado = true;
              fillInfoWindow(evento, j);
            }
        }
        while(!existe){

          if (markers[cont] == null){
            existe = true;
            var markerPos = new google.maps.LatLng(evento.latitud, evento.longitud);
            if (evento.event_type == "limitado"){
              markers[cont] = new google.maps.Marker({
                map: map,
                animation: google.maps.Animation.DROP,
                position: markerPos,
                icon: eventoImg
              });
            }else{
              markers[cont] = new google.maps.Marker({
                map: map,
                animation: google.maps.Animation.DROP,
                position: markerPos,
                icon: paradaImg
              });
            }
            
            markers[cont].usado = true;
            fillInfoWindow(evento, cont);
            initMarkerListeners(evento, cont);
          }
          else{
            cont = cont+1;
          }
   
      }
    }


    for(var x = 0; x < markers.length; x++){
        if(markers[x] != null && !markers[x].usado){
            markers[x].setMap(null);
            markers[x].id = null;
            markers[x] = null;
        }
    }




    }


    function fillInfoWindow(evento,cont) {

      var infoWindow = new google.maps.InfoWindow();    
      markers[cont].id = evento.id;

      if (evento.event_type == "limitado"){
        infoWindow.setContent('<p><center><b><u>'+evento.event_name+'</u></b></center></p>' +
        '<p><b>Empieza: </b>' + evento.ini_date + '</p>' + 
        '<p><b>Termina: </b>' + evento.exp_date + '</p>' + 
        '<p><b>Consigue: </b>' + evento.reward + '</p>' + 
        '<center><button onclick="location.href=\'#/app/evento/'+evento.id+'\';">Participar</button></center>'
        );
      }else{
        infoWindow.setContent('<p><center><b><u>'+evento.event_name+'</u></b></center></p>' +
        '<p><b>Tiempo de recarga: </b>' + evento.cooldown + '</p>' +
        '</p><p><b>Consigue: </b>' + evento.reward + '</p>'
        );
        if(!evento.last_use){
          infoWindow.setContent(infoWindow.getContent() + '<p>Has recogido el premio</p>');
        } else {
          infoWindow.setContent(infoWindow.getContent() + '<p><b>Disponible: </b>'+evento.last_use+'</p>');
        }
      }

      markers[cont].infoWindow = infoWindow;

    }

    function initMarkerListeners(evento, cont){

      google.maps.event.addListener(markers[cont],'click', function () {
          updateMap(markers[cont],evento);  
          
      });

    }


    function getEvents(){

      $http({
        method: 'GET',
        url: ApiEndpoint.url+ 'mapa/usr='+$localstorage.get('name')+'&lat='+latLng.lat+'&lng='+latLng.lng,
      }).then(function successCallback(response) {
          $scope.eventos = [];
          for(var r in response.data) {
            var evento = response.data[r];
            $scope.eventos.push(evento);
               
          }
          createMarkers();  


      }, function errorCallback(response) {
          console.log("ERROR");
      });     

    }



    function updateMap(marker,event){

      $http({
        method: 'GET',
        url: ApiEndpoint.url+ 'mapa/usr='+$localstorage.get('name')+'&lat='+latLng.lat+'&lng='+latLng.lng,
      }).then(function successCallback(response) {
          $scope.eventos = [];
          for(var r in response.data) {
            var evento = response.data[r];
            $scope.eventos.push(evento);       
          }
          createMarkers();


          for(var i = 0; i < $scope.eventos.length; i++){
            if($scope.eventos[i].id == event.id){
              event = $scope.eventos[i]
            }
          } 


          if(infoWindowClose){
            infoWindowClose.close();
          }       
          infoWindowClose = marker.infoWindow
          marker.infoWindow.open(map, marker);
          
          if(!event.last_use){
            addStop(event.id);
          }



      }, function errorCallback(response) {
          console.log("ERROR");
      });     

    }


    function addStop(id){
      $http({
        method: 'POST',
        url: ApiEndpoint.url+ 'eventoParada/',
        data: id,
      }); 

    }
    

  })

  // Code you want executed every time view is closed
  $scope.$on('$ionicView.beforeLeave', function(){
      clearInterval(timer);
      clearInterval(timer2);
  });
  
})
