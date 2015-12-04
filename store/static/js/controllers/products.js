/*
  Logs a user in
*/

(function(){
  'use strict';

  // Create the login controller
  angular.module('app').controller('ProductsController', ProductsController);

  ProductsController.$inject = ['ProductsService', '$location'];

  function ProductsController(ProductsService, $location, $scope){
    var products = this;

    products.products = undefined;
    products.sort = "";
    products.query = "";


    products.getAll = function(){
      ProductsService.getAll(function(res){
        console.log(res);
        if(res.status === 'good'){
          products.products = res.data;
        }else{
          products.products = undefined;
        }
      });
    };

    products.setSortMethod = function(sort){
      products.sort = sort;
    };

    products.search = function(){
      ProductsService.search(products.query, products.sort, function(res){
        console.log(res);
        if(res.status === 'good'){
          products.products = res.data;
        }else{
          products.products = undefined;
        }
      });
    };

    products.getAll();
  }
})();
