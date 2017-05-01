angular.module('myIonicApp')

.factory('$localstorage', ['$window', function($window) {
  return {
    set: function(key, value) {
      $window.localStorage[key] = value;
    },
    get: function(key, defaultValue) {
      return $window.localStorage[key] || defaultValue;
    },
    setObject: function(key, value) {
      $window.localStorage[key] = JSON.stringify(value);
    },
    getObject: function(key) {
      return JSON.parse($window.localStorage[key] || '{}');
    },
    clear: function () {
      $window.localStorage.clear();
    }
  }
}])

.factory('Token', function($q,$http,ApiEndpoint,$localstorage,$ionicPopup,$state) {

    function checkToken() {
      var data = {username : $localstorage.get('name'), token : $localstorage.get('token')};
      var success = "false";
      $http({
        method:'POST',
        url: ApiEndpoint.url+'checkLogin/', 
        data: data,
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
          }

      }).then(function successCallback(response) {
        success = response.data;
        if(success == "false"){
          var alertPopup = $ionicPopup.alert({
            title: '<u>Su sesión ha caducado</u>',
            template: 'Necesita volver a logear para usar la aplicación.'
          })
          $state.go('app.login');
        }
        return success
        

      }, function errorCallback(response) {
        console.log("TOKEN ERROR");
      })
      return success 
    }

    return {
      isToken : checkToken
    }

    

})

.factory('FileService', function($http,ApiEndpoint,$ionicPopup) {

 
  function getFileContentAsBase64(path,callback){
    window.resolveLocalFileSystemURL(path, gotFile, fail);
            
    function fail(e) {
          alert('Cannot found requested file');
    }

    function gotFile(fileEntry) {
           fileEntry.file(function(file) {
              var reader = new FileReader();
              reader.onloadend = function(e) {
                   var content = this.result;
                   callback(content);
              };
              // The most important point, use the readAsDatURL Method from the file plugin
              reader.readAsDataURL(file);
           });
    }
  }


 
  function addImage(img, path, brand) {

	  getFileContentAsBase64(path+img,function(base64Image){

      $http({
        method:'POST',
        url: ApiEndpoint.url+'sendImage/', 
        data: {'img' : JSON.stringify(base64Image), 'brand' : brand},

      }).then(function successCallback(response) {
        result = response.data
        if(result == "true"){
          var alertPopup = $ionicPopup.alert({
            title: '<u>Felicidades</u>',
            template: 'Has logrado la recompensa.'
          })
        } else {
          var alertPopup = $ionicPopup.alert({
            title: '<u>Lo siento</u>',
            template: 'Esa imagen no es la que buscábamos. Inténtelo de nuevo.'
          })
        }

      }, function errorCallback(response) {
        console.log("PHOTO ERROR");
      }) 

	  });
  };
 
  return {
    storeImage: addImage,
  }
})

.factory('ImageService', function($cordovaCamera, FileService, $q, $cordovaFile) {
 
  function makeid() {
    var text = '';
    var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
 
    for (var i = 0; i < 5; i++) {
      text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
  };
 
  function optionsForType() {
    var source;
    source = Camera.PictureSourceType.CAMERA;

    return {
      destinationType: Camera.DestinationType.FILE_URI,
      sourceType: source,
      encodingType: Camera.EncodingType.JPEG,
      popoverOptions: CameraPopoverOptions,
      saveToPhotoAlbum: false
    };
  }
 
  function saveMedia(brand) {
    return $q(function(resolve, reject) {

      var options = optionsForType();
 
      $cordovaCamera.getPicture(options).then(function(imageUrl) {
        var name = imageUrl.substr(imageUrl.lastIndexOf('/') + 1);
        var namePath = imageUrl.substr(0, imageUrl.lastIndexOf('/') + 1);
        var newName = makeid() + name;	
		
        $cordovaFile.copyFile(namePath, name, cordova.file.dataDirectory, newName)
          .then(function(info) {
            FileService.storeImage(newName, cordova.file.dataDirectory, brand);
            resolve();
          }, function(e) {
            reject();
          });
      });
    })
  }
  return {	
    takePhoto: saveMedia
  }
  
});