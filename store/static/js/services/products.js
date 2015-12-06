(function(){

  'use strict';

  angular.module('app').factory('ProductsService', ProductsService);

  ProductsService.$inject = ['$http'];

  function ProductsService($http){
    return {
      'search': function(query, sort, success){
          $http({
            method: 'POST',
            url: '/api/products/search/',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            transformRequest: function(obj) {
                var str = [];
                for(var p in obj)
                str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                return str.join("&");
            },
            data: {
              'query': query,
              'sort': sort
            }
          })
          .success(function(res){
            success(res);
          });
      },
      'getAll': function(success){
          $http({
            method: 'POST',
            url: '/api/products/',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            transformRequest: function(obj) {
                var str = [];
                for(var p in obj)
                str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                return str.join("&");
            }
          })
          .success(function(res){
            success(res);
          });
      },
      'addProduct': function(productName, price, desc, stock_quantity, callback){
        $http({
          method: 'POST',
          url: 'api/product/add/',
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          transformRequest: function(obj) {
            var str = [];
            for(var p in obj)
            str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
            return str.join("&");
          },
          data: {
            'name': productName,
            'price': price,
            'description': desc,
            'stock_quantity': stock_quantity
          }
        })
        .success(function(res){
          callback(res);
        });
      },

    };
  }
})();
