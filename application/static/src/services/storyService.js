'use strict';

var StoryService = Class.extend({
  $q: null,
  $http: null,
  baseUrl: 'api',

  /**
   * Init class
   */
  init: function($q, $http) {
    this.$q = $q;
    this.$http = $http;
  },

  /**
   * Pull a list of the latest stories
   */
  getStories: function(cursor) {
    var deferred = this.$q.defer();

    this.$http({
      method: 'GET',
      url: this.baseUrl + '/entries',
      params: {
        cursor: cursor
      }
    }).then(function(data) {
      deferred.resolve(data.data);
    }, function(err) {
      console.error(err); //TODO: real error handling
      deferred.reject(err);
    });

    return deferred.promise;
  }

});

(function() {
  var StoryServiceProvider = Class.extend({
    $get: function($q, $http) {
      return new StoryService($q, $http);
    }
  });

  angular.module('story.StoryService',[])
    .provider('StoryService', StoryServiceProvider);
}());
