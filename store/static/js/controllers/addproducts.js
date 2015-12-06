/*
Controller for adding product to database
*/
(function(){
	'use strict';

	angular.module('app').controller('AddingController', AddingController);

	AddingController.$inject = ['ProductsService', '$location'];

	function AddingController(ProductsService, $location, $scope){
		var products = this;
		
		products.products = undefined;
		products.productName = "";
		products.price = 0;
		products.desc = "";
		products.stock_quantity = 0;
		

		products.addProduct = function(name, description, price, stock_quantity){
			products.name = name;
			products.description = description;
			products.price = price;
			products.stock_quantity = stock_quantity;
			ProductsService.addProduct(products.name, products.description, products.price, products.stock_quantity, function(res){
				console.log(res);
				if(res.status === 'good'){
					products.products = res.data;
				}else{
					products.products = undefined;
				}
			})
		}
	}

})
