/*
  Logs a user in
*/

(function(){
  'use strict';

  // Create the login controller
  angular.module('app').controller('LoginController', LoginController);

  LoginController.$inject = ['AuthService', '$location', '$rootScope'];

  function LoginController(AuthService, $location, $rootScope){
    var login = this;
    login.login = function(){
      login.loading = true;

      AuthService.login(login.email, login.password, function(res){
        if(res.status === 'good'){
          login.error = '';
          $rootScope.name = res.data.name;
          localStorage.setItem('name', res.data.name);
          $location.path('/');
        }else{
          login.error = res.message;
        }
        login.loading = false;
      });
    };

    login.register = function(){
      if(login.password !== login.password2){
        login.error = 'Passwords do not match!';
        return false;
      }

      login.loading = true;

      AuthService.register(login.name, login.password, login.email, login.address, function(res){
        console.log(res);
        if(res.status === 'good'){
          login.error = '';
          $location.path('/login/');
        }else{
          login.error = res.message;
        }
        login.loading = false;
      });
    }
  }
})();
