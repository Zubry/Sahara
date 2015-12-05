(function(){

  'use strict';

  angular.module('app').factory('ProductService', ProductService);

  ProductService.$inject = ['$http'];

  function ProductService($http){
    return {
      'me': function(success){
        return $http.get('/api/user/me').then(success);
      },
      'get': function(id){
        return $http.get('/api/product/'+id+'/');
      },
      'remove': function(id){
        return $http({
          method: 'POST',
          url: '/api/product/remove/',
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          transformRequest: function(obj) {
              var str = [];
              for(var p in obj)
              str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
              return str.join("&");
          },
          data: {
            'id': id
          }
        });
      },
      'update': function(id, name, description, price, stock_quantity){
        return $http({
          method: 'POST',
          url: '/api/product/update/',
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          transformRequest: function(obj) {
              var str = [];
              for(var p in obj)
              str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
              return str.join("&");
          },
          data: {
            'id': id,
            'name': name,
            'description': description,
            'price': price,
            'stock_quantity': stock_quantity
          }
        });
      },
      'order': function(id, quantity){
        if(!quantity){
          quantity = 1;
        }

        return $http({
          method: 'POST',
          url: '/api/product/order/',
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          transformRequest: function(obj) {
              var str = [];
              for(var p in obj)
              str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
              return str.join("&");
          },
          data: {
            'id': id,
            'quantity': quantity
          }
        });

      },
      'supply': function(id, supplier_id){
        return $http({
          method: 'POST',
          url: '/api/product/supply/',
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          transformRequest: function(obj) {
              var str = [];
              for(var p in obj)
              str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
              return str.join("&");
          },
          data: {
            'product': id,
            'supplier': supplier_id
          }
        });
      },
      'activate': function(id){
        return $http({
          method: 'POST',
          url: '/api/products/activate/',
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          transformRequest: function(obj) {
              var str = [];
              for(var p in obj)
              str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
              return str.join("&");
          },
          data: {
            'id': id
          }
        });
      },
      'deactivate': function(id){
        return $http({
          method: 'POST',
          url: '/api/products/deactivate/',
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          transformRequest: function(obj) {
              var str = [];
              for(var p in obj)
              str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
              return str.join("&");
          },
          data: {
            'id': id
          }
        });
      },
      'getSuppliers': function(){
        return $http.get('/api/suppliers/');
      }
    };
  }
})();
