'use strict';

/**
 * Story List Directive
 *
 * A simple directive to handle listing stories and toggling the
 * read state on the individual stories (Might be worth moving
 * the read state toggling functionality into a StoryListItemDirective)
 */
var StoryListDirective = BaseDirective.extend({
  storyModel: null,

  /**
   * Init Class
   */
  init: function($scope, Events, StoryModel) {
    this.storyModel = StoryModel;

    this._super($scope, Events);
  },

  /**
   * Add event listener for ENTRIES_LOADED which is fired when the
   * StoryModel has a new set of stories.
   */
  addListeners: function() {
    this._super();

    this.storiesLoaded = this.storiesLoaded.bind(this);
    this.events.addEventListener(models.events.ENTRIES_LOADED, this.storiesLoaded);
  },

  /**
   * Setup scope
   */
  setupScope: function() {
    this.$scope.stories = [];
    this.$scope.meta = {};
    this.$scope.loading = true;

  },

  /**
   * Unbind event listeners on class destroy
   */
  destroy: function() {
    this._super();
    this.events.removeEventListener(models.events.ENTRIES_LOADED, this.storiesLoaded);
  },

  /**
   * Event handler for ENTRIES_LOADED, hides the loading state
   * and sets the new stories on the scope
   */
  storiesLoaded: function() {
    this.$scope.loading = false;

    var data = this.storyModel.getStories();
    this.$scope.stories = data.entries;
    this.$scope.meta = data.meta;
  }

});

angular.module('storyList',[])
  .directive('storyList', function(Events, StoryModel) {
  return {
    restrict: 'E',
    isolate: true,
    link: function($scope) {
      new StoryListDirective($scope, Events, StoryModel);
    },
    scope: true,
    templateUrl: 'partials/storyList/storyList.html'
  };
});
