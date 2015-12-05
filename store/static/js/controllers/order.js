(function(){
  'use strict';

  // Create the login controller
  angular.module('app').controller('OrderController', OrderController);

  OrderController.$inject = ['OrderService', '$location', '$scope'];

  function OrderController(OrderService, $location, $scope){
    $scope.cart = {};

    OrderService.get()
      .then(function(res){
        $scope.cart = res.data.data;
      });

    $scope.remove = function(id){
      OrderService.remove_item(id)
        .then(OrderService.get)
        .then(function(res){
          $scope.cart = res.data.data;
        });
    };

    $scope.clear = function(){
      OrderService.clear()
        .then(OrderService.get)
        .then(function(res){
          $scope.cart = res.data.data;
        });
    };

    $scope.checkout = function(){
      OrderService.checkout()
        .then(function(){
          $location.path('/products/');
        });
    };

    $scope.totalPrice = function(){
      return $scope.cart.products.reduce(function(a, b){
        return a + (b.product_quantity * b.product_price);
      }, 0);
    }
  }

})();
