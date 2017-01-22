'use strict';
var app = angular.module('snifferApp', ['ngRoute', 'ngResource', 'd3', 'entryCtrl', 'entryServices', 'lineChartDir']);

/*
 * Config
 */
app.config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
    $routeProvider
	   .when('/dashboard', {
	       controller: 'EntryListCtrl',
	       templateUrl: '/dashboard/partials/entry-list.html'
	   })
	   .otherwise({ redirectTo: '/home' });
    $locationProvider.html5Mode({
        enabled: true,
        requireBase: false /*specify a default URL and a default target for all links on a page*/
    });
}]);