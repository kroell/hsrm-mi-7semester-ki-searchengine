var MainCtrl = function($scope, $http){

	var url = '/search-spiegel/Frontend/api/Searcher.py';

	$scope.loading = true;
	 $http.post(url, { foo: 'bar' }).success(function(response)
	  {
	    $scope.response = response;
	    $scope.loading = false;
	  });
};



