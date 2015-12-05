(function(){
  'use strict';

  // Create the login controller
  angular.module('app').controller('ProductController', ProductController);

  ProductController.$inject = ['ProductService', 'UserService', '$location', '$routeParams', '$scope'];

  function ProductController(ProductService, UserService, $location, $routeParams, $scope){
    $scope.product_id = $routeParams.product_id;
    $scope.product = {};
    $scope.profile = {};

    UserService.me(function(res){
      if(res.data.status === 'good'){
        $scope.profile.name = res.data.data.name;
        $scope.profile.email = res.data.data.email;
        $scope.profile.address = res.data.data.address;
        $scope.profile.staff = res.data.data.staff;
      }else{
        profile.error = 'Error loading profile information!';
      }
    });

    ProductService.get($scope.product_id)
      .then(function(res){
        if(res.data.status === 'good' && res.data.data[0]){
          $scope.product = res.data.data[0];
          $scope.product.quantity = 1;
          console.log($scope.product);
        }
      });

    $scope.update_name = function(){
      ProductService.update($scope.product.id, $scope.product.name, '', '', '');
    };

    $scope.update_description = function(){
      ProductService.update($scope.product.id, '', $scope.product.description, '', '');
    };

    $scope.update_price = function(){
      ProductService.update($scope.product.id, '', '', $scope.product.price, '');
    };

    $scope.update_stock_quantity = function(){
      ProductService.update($scope.product.id, '', '', '', $scope.product.stock_quantity);
    };

    $scope.delete_item = function(){
      ProductService.remove($scope.product.id)
        .then(function(){
          $location.path('/products/');
        });
    };

    $scope.activate = function(){
      ProductService.activate($scope.product.id);
    };

    $scope.deactivate = function(){
      ProductService.deactivate($scope.product.id);
    };

    $scope.order = function(){
      ProductService.order($scope.product.id, $scope.product.quantity)
        .then(function(){
          $location.path('/cart/');
        });
    };
  }

})();
