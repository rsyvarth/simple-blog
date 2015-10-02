'use strict';

var UserService = Class.extend({
  $q: null,
  $http: null,
  baseUrl: config.baseUrl + 'api',

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
  getSelf: function() {
    var deferred = this.$q.defer();

    this.$http({
      method: 'GET',
      url: this.baseUrl + '/users/self'
    }).then(function(data) {
      deferred.resolve(data.data);
    }, function(err) {
      console.error(err); //TODO: real error handling
      deferred.reject(err);
    });

    return deferred.promise;
  },

    /*
     *update my status as a user
     */
  updateSelf: function(data) {
    var deferred = this.$q.defer();

    this.$http({
      method: 'PUT',
      data: data,
      url: this.baseUrl + '/users/self'
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
  var UserServiceProvider = Class.extend({
    $get: function($q, $http) {
      return new UserService($q, $http);
    }
  });

  angular.module('user.UserService',[])
    .provider('UserService', UserServiceProvider);
}());
