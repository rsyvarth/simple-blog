'use strict';

/**
 * Home Controller
 *
 * Manages the home page and controls loading data for the
 * the story list directive.
 */
var ViewController = Class.extend({
  $scope: null,
  events: null,
  storyModel: null,
  $stateParams: null,

  /**
   * Init class
   */
  init: function($scope, Events, StoryModel, $stateParams) {
    this.$scope = $scope;
    this.events = Events;
    this.storyModel = StoryModel;
    this.$stateParams = $stateParams;

    this.setupScope();
  },

  setupScope: function() {
    this.storyModel.loadStory(this.$stateParams.postId);
    this.$scope.loading = true;

    this.storyLoaded = this.storyLoaded.bind(this);
    this.events.addEventListener(models.events.ENTRY_LOADED, this.storyLoaded);
  },

  storyLoaded: function() {
    var data = this.storyModel.getStory();
    this.$scope.loading = false;
    this.$scope.story = data;
  }

});

ViewController.$inject = ['$scope', 'Events', 'StoryModel', '$stateParams'];
