angular.module('PropertyViewApp',[])
   .controller('PropertyViewController', ['$scope','$http',function($scope,$http){
       $http({
            method: 'GET',
            url: 'data?state=ca'
        }).then(function successCallback(response) {
                $scope.properties = response.data;
            }, function errorCallback(response) {
                
            });
   }]);