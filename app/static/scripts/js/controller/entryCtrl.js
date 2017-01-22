/*Module entryCtrl*/
var app = angular.module('entryCtrl', []);

/*List of all entries*/
app.controller('EntryListCtrl', ['$scope', 'Entry', function ($scope, Entry) {
    $scope.entries = {};
    $scope.lineData = [];
    var dataArray = [];
    for (i = 0; i < 100; i+=0.1) {
        dataArray.push({ x: i, y: Math.sin(i) })
    }
    $scope.lineData.push(dataArray);

    $scope.initEntries = function()
    {
        $scope.entries = Entry.query();
    }

    var sincos = 'cos'
    $scope.buttonClicked = function ()
    {
        dataArray = [];
        if (sincos == 'cos') {
            for (i = 0; i < 100; i += 0.1) {
                dataArray.push({ x: i, y: 2*Math.cos(i/5) })
            }
            $scope.lineData[0] = dataArray;
            sincos = 'cos5'
        }
        else {
            for (i = 0; i < 100; i += 0.1) {
                dataArray.push({ x: i, y: Math.cos(i) })
            }
            $scope.lineData[0] = dataArray;
            sincos = 'cos'
        }
    }
}]);

/*Entry detail*/
app.controller('EntryDetailCtrl', ['$scope', '$routeParams', 'Entry', function ($scope, $routeParams, Entry) {
    $scope.entry = Entry.get({ entryId: $routeParams.entryId }, function (entry) {
        
    });
}]);