/*
  Control's a user's profile
*/

(function(){
  'use strict';

  // Create the profile controller
  angular.module('app').controller('ProfileController', ProfileController);

  ProfileController.$inject = ['UserService', '$location', '$rootScope'];

  function ProfileController(UserService, $location, $rootScope){
    var profile = this;

    UserService.me(function(res){
      if(res.data.status === 'good'){
        profile.name = res.data.data.name;
        profile.email = res.data.data.email;
        profile.address = res.data.data.address;
        if(profile.address === 'undefined'){
          profile.address = '';
        }

      }else{
        profile.error = 'Error loading profile information!';
        $location.path('/login/');
      }
    });

    profile.delete_account = function(){
      profile.delete_loading = true;

      var password = prompt('Please confirm your password before you can delete your account.');

      if(password !== null){
        UserService.delete(password, function(res){
          if(res.status === 'good'){
            $rootScope.name = 'Guest';
            localStorage.removeItem('name');
            $location.path('/');
          }else{
            profile.error = res.message;
          }
          profile.delete_loading = false;
        });
      }
    };

    profile.update_name = function(){
      profile.name_loading = true;

      UserService.update_name(profile.name, function(res){
        console.log(res);
        if(res.status === 'good'){
          $rootScope.name = res.data.name;
          localStorage.setItem('name', res.data.name);
        }else{
          profile.error = res.message;
        }
        profile.name_loading = false;
      });
    };

    profile.update_address = function(){
      profile.address_loading = true;

      UserService.update_address(profile.address, function(res){
        if(res.status === 'good'){
          profile.error = '';
        }else{
          profile.error = res.message;
        }
        profile.address_loading = false;
      });
    };

    profile.update_email = function(){
      profile.email_loading = true;

      UserService.update_email(profile.email, function(res){
        if(res.status === 'good'){
          profile.error = '';
        }else{
          profile.error = res.message;
        }
        profile.email_loading = false;
      });
    };

    profile.update_password = function(){
      var current_password = prompt('Please confirm your password to change it');

      if(current_password === null){
        return false;
      }

      profile.password_loading = true;

      UserService.update_password(current_password, profile.password, function(res){
        console.log(res);
        if(res.status === 'good'){
          alert('changed password');
          profile.error = '';
        }else{
          profile.error = res.message;
        }
        profile.password_loading = false;
      });
    };

    profile.logout = function(){
      UserService.logout(function(res){
        $rootScope.name = 'Guest';
        localStorage.removeItem('name');
        $location.path('/');
      });
    };
  }
})();
