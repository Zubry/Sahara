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
      .when('/product/:product_id/', {
        'templateUrl': '/static/templates/product.html',
        'controller': 'ProductController',
        'controllerAs': 'product'
      })
      .when('/staff/', {
        'templateUrl': '/static/templates/main.html',
        'controller': 'LoginController',
        'controllerAs': 'login'
      })
      .when('/cart/', {
        'templateUrl': '/static/templates/cart.html',
        'controller': 'OrderController',
        'controllerAs': 'order'
      })
      .when('/carts/', {
        'templateUrl': '/static/templates/cart.html',
        'controller': 'StaffOrderController',
        'controllerAs': 'order'
      })
      .when('/cart/:id/', {
        'templateUrl': '/static/templates/staff-cart.html',
        'controller': 'StaffOrderController',
        'controllerAs': 'order'
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
