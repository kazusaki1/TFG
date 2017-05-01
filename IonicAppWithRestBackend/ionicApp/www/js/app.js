angular.module('myIonicApp', ['ionic', 'myIonicApp.controllers', 'ngCordova', 'ionic-material', 'ionMdInput'])

.constant('ApiEndpoint',{
  url: 'http://192.168.1.33:8000/'
})
.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    if (window.cordova && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
      cordova.plugins.Keyboard.disableScroll(true);

      $httpProvider.defaults.useXDomain=true;
      delete $httpProvider.defaults.headers.common['X-Requested-With'];
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
  .state('app.register', {
      url: '/register',
      views: {
        'menuContent': {
            templateUrl: 'templates/register.html',
            controller: 'RegisterCtrl'
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
  .state('app.perfil',{
    url: '/perfil',
    views: {
        'menuContent': {
            templateUrl: 'templates/perfil.html',
            controller: 'PerfilCtrl'
        }
    }
  })
  .state('app.recompensa',{
    url: '/recompensa',
    views: {
        'menuContent': {
            templateUrl: 'templates/recompensa.html',
            controller: 'RecompensaCtrl'
        }
    }
  })

  // if none of the above states are matched, use this as the fallback
  $urlRouterProvider.otherwise( function($injector, $location) {
            var $state = $injector.get("$state");
            $state.go("app.login");
        });
});





