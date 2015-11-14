/*
  Perform User operations
*/

(function(){
  'use strict';


  // Create a User service
  angular.module('app').factory('UserService', UserService);

  UserService.$inject = ['$http'];

  // This is essentially a client-side ORM. This is where you can perform the standard CRUD operations on a user
  function UserService($http){
    return {
      // Gets information about the user
      'me': function(success){
        return $http.get('/api/user/me').then(success);
      },
      'logout': function(success){
        return $http.get('/api/auth/logout').then(success);
      },
      'delete': function(password, success){
          $http({
            method: 'POST',
            url: '/api/user/me/delete/',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            transformRequest: function(obj) {
                var str = [];
                for(var p in obj)
                str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                return str.join("&");
            },
            data: {
              'password': password
            }
          })
          .success(function(res){
            success(res);
          });
      },
      'update_email': function(email, success){
          $http({
            method: 'POST',
            url: '/api/user/me/email/',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            transformRequest: function(obj) {
                var str = [];
                for(var p in obj)
                str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                return str.join("&");
            },
            data: {
              'email': email
            }
          })
          .success(function(res){
            success(res);
          });

      },
      'update_address': function(address, success){
          $http({
            method: 'POST',
            url: '/api/user/me/address/',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            transformRequest: function(obj) {
                var str = [];
                for(var p in obj)
                str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                return str.join("&");
            },
            data: {
              'address': address
            }
          })
          .success(function(res){
            success(res);
          });

      },
      'update_name': function(name, success){
          $http({
            method: 'POST',
            url: '/api/user/me/name/',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            transformRequest: function(obj) {
                var str = [];
                for(var p in obj)
                str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                return str.join("&");
            },
            data: {
              'name': name
            }
          })
          .success(function(res){
            success(res);
          });

      },
      'update_password': function(current_password, new_password, success){
          $http({
            method: 'POST',
            url: '/api/user/me/password/',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            transformRequest: function(obj) {
                var str = [];
                for(var p in obj)
                str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                return str.join("&");
            },
            data: {
              'current_password': current_password,
              'new_password': new_password
            }
          })
          .success(function(res){
            success(res);
          });
      }
    };
  }
})()
