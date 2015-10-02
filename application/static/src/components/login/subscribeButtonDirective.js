'use strict';

var subscribeButtonDirective = BaseDirective.extend({
  userModel: null,

  /**
   * Init Class
   */
  init: function($scope, Events, UserModel) {
    this.userModel = UserModel;

    this._super($scope, Events);
    this.userModel.loadSelf();
  },

  /**
   * Add event listener for USER_LOADED which is fired when the
   * StoryModel has a new set of stories.
   */
  addListeners: function() {
    this._super();

    this.userLoaded = this.userLoaded.bind(this);
    this.events.addEventListener(models.events.USER_LOADED, this.userLoaded);
  },

  /**
   * Setup scope
   */
  setupScope: function() {
    this.$scope.user = {};

    this.$scope.subscribe = this.subscribe.bind(this);
    this.$scope.unsubscribe = this.unsubscribe.bind(this);

  },

  /**
   * Unbind event listeners on class destroy
   */
  destroy: function() {
    this._super();
    this.events.removeEventListener(models.events.USER_LOADED, this.userLoaded);
  },

  /**
   * Event handler for USER_LOADED, hides the loading state
   * and sets the new stories on the scope
   */
  userLoaded: function() {
    var data = this.userModel.getSelf();
    this.$scope.user = data;
    console.log("user loader called", data)
  },

  subscribe: function() {
    this.userModel.subscribe(true);
  },

  unsubscribe: function() {
    this.userModel.subscribe(false);
  }

});

angular.module('subscribeButton',[])
  .directive('subscribeButton', function(Events, UserModel) {
  return {
    restrict: 'E',
    isolate: true,
    link: function($scope) {
      new subscribeButtonDirective($scope, Events, UserModel);
    },
    scope: true,
    templateUrl: 'partials/subscribe/subscribeButton.html'
  };
});
