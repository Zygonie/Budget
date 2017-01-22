var app = angular.module('entryServices', ['ngResource']);

app.factory('Entry', ['$resource',
  function ($resource) {
      return $resource('/api/entry/:entryId',
          {},
          { query: { method: 'GET', params: { entryId: '@entryId' }, isArray: true } });
  }]);