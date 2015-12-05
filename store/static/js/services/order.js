(function(){

  'use strict';

  angular.module('app').factory('OrderService', OrderService);

  OrderService.$inject = ['$http'];

  function OrderService($http){
    return {
      'get': function(){
        return $http.get('/api/order/');
      },
      'remove_item': function(id){
        return $http({
          method: 'POST',
          url: '/api/order/remove-item/',
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
      'clear': function(){
        return $http({
          method: 'POST',
          url: '/api/order/clear/',
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          transformRequest: function(obj) {
              var str = [];
              for(var p in obj)
              str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
              return str.join("&");
          }
        });
      },
      'checkout': function(){
        return $http({
          method: 'POST',
          url: '/api/order/checkout/',
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          transformRequest: function(obj) {
              var str = [];
              for(var p in obj)
              str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
              return str.join("&");
          }
        });
      },
      'search': function(query){
        return $http({
          method: 'POST',
          url: '/api/orders/search/',
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          transformRequest: function(obj) {
              var str = [];
              for(var p in obj)
              str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
              return str.join("&");
          },
          data: {
            'email': query
          }
        });
      },
      'get_by_id': function(id){
        return $http.get('/api/order/'+id+'/');
      },
      'remove_item_by_id': function(cart_id, id){
        return $http({
          method: 'POST',
          url: '/api/order/'+cart_id+'/remove-item/',
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
      'update_item_by_id': function(user_id, id, quantity){
        return $http({
          method: 'POST',
          url: '/api/order/'+user_id+'/update-item/',
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
      'clear_by_id': function(cart_id, id){
        return $http({
          method: 'POST',
          url: '/api/order/'+cart_id+'/clear/',
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
      }
    }
  }

})();
