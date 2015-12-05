(function(){
  'use strict';

  // Create the login controller
  angular.module('app').controller('StaffOrderController', StaffOrderController);

  StaffOrderController.$inject = ['OrderService', 'UserService', '$location', '$routeParams', '$scope'];

  function StaffOrderController(OrderService, UserService, $location, $routeParams, $scope){
      $scope.cart_id = $routeParams.id;

      $scope.profile = {};
      $scope.cart = {};


      UserService.me(function(res){
        if(res.data.status === 'good'){
          $scope.profile.name = res.data.data.name;
          $scope.profile.email = res.data.data.email;
          $scope.profile.address = res.data.data.address;
          $scope.profile.staff = res.data.data.staff;
        }else{
          $scope.profile.error = 'Error loading profile information!';
        }
      });

      OrderService.get_by_id($scope.cart_id)
        .then(function(res){
          if(res.data.status === 'good'){
            $scope.cart = res.data;
              console.log($scope.cart);
          }else{
            $scope.error = 'No cart found!';
          }
        });

      $scope.remove_item_by_id = function(product_id){
        OrderService.remove_item_by_id($scope.cart_id, product_id)
          .then(function(){
            return OrderService.get_by_id($scope.cart_id);
          });
      };

      $scope.clear_by_id = function(){
        OrderService.clear_by_id($scope.cart_id)
          .then(function(){
            return OrderService.get_by_id($scope.cart_id);
          });
      };

      $scope.update_by_id = function(active, user_id, quantity, product_id){
        if(active){
          return false;
        }
        OrderService.update_item_by_id(user_id, product_id, quantity)
          .then(function(){
            return OrderService.get_by_id($scope.cart_id);
          });
      };
  }

})();
