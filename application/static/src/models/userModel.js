'use strict';

/**
 * Define the USER_LOADED event which this model emits
 */
namespace('models.events').USER_LOADED = 'UserModel.USER_LOADED';

/**
 * User Model
 *
 * Pulls most popular user plus scrapes each user's target
 * url in order to retrieve embed information.
 */
var UserModel = Class.extend({
  user: {},
  events: null,
  $q: null,
  userService: null,

  /**
   * Init class
   */
  init: function(Events, $q, UserService) {
    this.events = Events;
    this.$q = $q;
    this.userService = UserService;
  },

  /**
   * Load the top user filtered by read state
   */
  loadSelf: function(cursor) {
    var deferred = this.$q.defer();

    this.userService.getSelf(cursor).then(function(data) {
      this.user = data;

      this.events.notify(models.events.USER_LOADED);
      deferred.resolve(this.user);

    }.bind(this));

    return deferred.promise;
  },

  /**
   * Get the list of user
   */
  getSelf: function() {
    return this.user;
  }
  
});

(function() {
  var UserModelProvider = Class.extend({
    $get: function(Events, $q, UserService) {
      return new UserModel(Events, $q, UserService);
    }
  });

  angular.module('user.UserModel',[])
    .provider('UserModel', UserModelProvider);
}());
