(function(){
  'use strict';

  var app = angular.module('app', ['ngRoute'])

  .config(function($routeProvider, $locationProvider){
    $locationProvider.hashPrefix('!');

    $routeProvider
      .when('/login/', {
        'templateUrl': '/static/templates/login.html',
        'controller': 'LoginController',
        'controllerAs': 'login'
      })
      .when('/register/', {
        'templateUrl': '/static/templates/register.html',
        'controller': 'LoginController',
        'controllerAs': 'login'
      })
      .when('/profile/', {
        'templateUrl': '/static/templates/profile.html',
        'controller': 'ProfileController',
        'controllerAs': 'profile'
      })
      .when('/products/', {
        'templateUrl': '/static/templates/products.html',
        'controller': 'ProductsController',
        'controllerAs': 'products'
      })
      .when('/product/', {
        'templateUrl': '/static/templates/product.html',
        'controller': 'LoginController',
        'controllerAs': 'login'
      })
      .when('/staff/', {
        'templateUrl': '/static/templates/main.html',
        'controller': 'LoginController',
        'controllerAs': 'login'
      })
      .when('/cart/', {
        'templateUrl': '/static/templates/main.html',
        'controller': 'LoginController',
        'controllerAs': 'login'
      })
      .when('/', {
        'templateUrl': '/static/templates/main.html',
        'controller': 'LoginController',
        'controllerAs': 'login'
      });
  })

  .run(function($rootScope) {
    $rootScope.name = localStorage.getItem('name') || "Guest";
  })
})();
