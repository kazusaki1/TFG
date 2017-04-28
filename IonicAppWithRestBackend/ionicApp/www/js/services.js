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


      var data = {username : $localstorage.get('name'), token : $localstorage.get('token')};
      var success = "False";
      var promise = $http({
        method:'POST',
        url: ApiEndpoint.url+'checkLogin/', 
        data: data,
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
          }

      }).then(function successCallback(response) {
        success = response.data;
        console.log(success)
        if(success == "true"){
          console.log("Token success: ",success)
        }else{
          var alertPopup = $ionicPopup.alert({
            title: '<u>Su sesión ha caducado</u>',
            template: 'Necesita volver a logear para usar la aplicación.'
          })
          $state.go('app.login');
        }
        

      }, function errorCallback(response) {
        console.log("TOKEN ERROR");
      }) 

    return {isToken : function() { return $q.all(promise).then(function(){
      return success
    })}}

})

.factory('FileService', function($http,ApiEndpoint,$ionicPopup) {
  var images;
  var IMAGE_STORAGE_KEY = 'images';
 
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

 
 
 
  function getImages() {
    var img = window.localStorage.getItem(IMAGE_STORAGE_KEY);
    if (img) {
      images = JSON.parse(img);
    } else {
      images = [];
    }
    return images;
  };
 
  function addImage(img, path) {
    images.push(img);
    window.localStorage.setItem(IMAGE_STORAGE_KEY, JSON.stringify(images));
	  getFileContentAsBase64(path+img,function(base64Image){
  		console.log(base64Image); 

      $http({
        method:'POST',
        url: ApiEndpoint.url+'sendImage/', 
        data: JSON.stringify(base64Image),

      }).then(function successCallback(response) {
        result = response.data
        console.log(result)
        if(result == "random"){
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
    images: getImages
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
 
  function optionsForType(type) {
    var source;
    switch (type) {
      case 0:
        source = Camera.PictureSourceType.CAMERA;
        break;
      case 1:
        source = Camera.PictureSourceType.PHOTOLIBRARY;
        break;
    }
    return {
      destinationType: Camera.DestinationType.FILE_URI,
      sourceType: source,
      allowEdit: true,
      encodingType: Camera.EncodingType.JPEG,
      popoverOptions: CameraPopoverOptions,
      targetWidth: 80,
      targetHeight: 80,
      saveToPhotoAlbum: false
    };
  }
 
  function saveMedia(type) {
    return $q(function(resolve, reject) {
      var options = optionsForType(type);
 
      $cordovaCamera.getPicture(options).then(function(imageUrl) {
        var name = imageUrl.substr(imageUrl.lastIndexOf('/') + 1);
        var namePath = imageUrl.substr(0, imageUrl.lastIndexOf('/') + 1);
        var newName = makeid() + name;	
		
        $cordovaFile.copyFile(namePath, name, cordova.file.dataDirectory, newName)
          .then(function(info) {
            FileService.storeImage(newName, cordova.file.dataDirectory);
            resolve();
          }, function(e) {
            reject();
          });
      });
    })
  }
  return {	
    handleMediaDialog: saveMedia
  }
  
});