/*
  Authenticate a user
*/

(function () {
  'use strict';

  // Create an authentication service
  angular.module('app').factory('AuthService', AuthService);

  AuthService.$inject = ['$http', 'UserService'];

  function AuthService($http, UserService){
    return {
      'login': function(email, password, callback){
        $http({
          method: 'POST',
          url: '/api/auth/login/',
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          transformRequest: function(obj) {
              var str = [];
              for(var p in obj)
              str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
              return str.join("&");
          },
          data: {
            'email': email,
            'password': password
          }
        })
        .success(function(res){
          callback(res);
        });
      },
      'register': function(name, password, email, address, callback){
        $http({
          method: 'POST',
          url: '/api/auth/register/',
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          transformRequest: function(obj) {
              var str = [];
              for(var p in obj)
              str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
              return str.join("&");
          },
          data: {
            'name': name,
            'password': password,
            'email': email,
            'address': address
          }
        })
        .success(function(res){
          callback(res);
        });
      }
    }
  }
})();
