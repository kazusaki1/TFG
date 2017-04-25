angular.module('myIonicApp', ['ionic', 'myIonicApp.controllers', 'ngCordova'])

.constant('ApiEndpoint',{
  url: 'http://192.168.1.33:8000/'
})
.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    if (window.cordova && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
      cordova.plugins.Keyboard.disableScroll(true);
    }
    if (window.StatusBar) {
      StatusBar.styleDefault();
    }
  });
})

.config(function($stateProvider, $urlRouterProvider) {
  $stateProvider

  .state('app', {
    url: '/app',
    abstract: true,
    templateUrl: 'templates/menu.html',
    controller: 'AppCtrl'
  })
  .state('app.login', {
      url: '/login',
      views: {
        'menuContent': {
            templateUrl: 'templates/login.html',
            controller: 'LoginCtrl'
        }
    }
      
  })
  .state('app.home',{
    url: '/home',
    views: {
        'menuContent': {
            templateUrl: 'templates/appHome.html',
            controller: 'MapCtrl'
            //controller: 'HomeCtrl'
        }
    }
  })
  .state('app.foto',{
    url: '/foto',
    views: {
        'menuContent': {
            templateUrl: 'templates/upload.html',
            controller: 'ImageCtrl'
        }
    }
  })
  .state('app.lista',{
    url: '/lista',
    views: {
        'menuContent': {
            templateUrl: 'templates/lista.html',
            controller: 'ListCtrl'
        }
    }
  })  
  .state('app.evento',{
    url: '/evento/:id',
    views: {
        'menuContent': {
            templateUrl: 'templates/evento.html',
            controller: 'EventCtrl'
        }
    }
  })

  // if none of the above states are matched, use this as the fallback
  $urlRouterProvider.otherwise('/app/login');
});





