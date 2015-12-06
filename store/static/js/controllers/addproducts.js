/*
Controller for adding product to database
*/
(function(){
	'use strict';

	angular.module('app').controller('AddingController', AddingController);

	AddingController.$inject = ['ProductsService', '$location', '$scope'];

	function AddingController(ProductsService, $location, $scope){
		$scope.products = undefined;
		$scope.name = "";
		$scope.price = 0;
		$scope.description = "";
		$scope.stock_quantity = 0;


		$scope.addProduct = function(){
			console.log($scope.description);
			ProductsService.addProduct($scope.name, $scope.price, $scope.description, $scope.stock_quantity, function(res){
				console.log(res);
				if(res.status === 'good'){
					$location.path('/products/');
				}else{
					$scope.products = undefined;
				}
			});
		};
	}

})();
