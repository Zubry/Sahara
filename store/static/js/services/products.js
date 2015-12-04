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

    };
  }
})();
