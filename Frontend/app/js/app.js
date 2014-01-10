var app = angular.module("app", []) 

app.config(function($routeProvider) {

  $routeProvider.when('/home', {
    templateUrl: 'home.html',
    controller: 'HomeController'
  });

  $routeProvider.when('/search', {
    templateUrl: 'search.html',
    controller: 'SearchController'
  });

  $routeProvider.otherwise({ redirectTo: '/home' });

});

app.config(function ($httpProvider) {
    $httpProvider.defaults.transformRequest = function(data){
        if (data === undefined) {
            return data;
        }
        return $.param(data);
    }
});


app.controller("HomeController", function($scope, $location) {

  window.scope = $scope;
  $scope.searchquery = "";

  

  $scope.doSearch = function() {

      if (Modernizr.localstorage) {
        window.localStorage.searchquery = $scope.searchquery;
      } 
     
      $location.path('/search');
  };

});



app.controller("SearchController", function($scope, $location, $http) {

  var query = window.window.localStorage.searchquery;
  var url = '/search-spiegel/Backend/Controller.py';
  var requestData = {'searchquery': query};

  var transform = function(data){
        return $.param(data);
    }

  $http.post(
    url , 
    requestData, 
    {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        //,transformRequest: transform
    })
    .success(function(responseData) {
        $scope.searchresponse = responseData;
    })
    .error(function (data, status, headers, config) {
      alert("error",status);
    });

});






