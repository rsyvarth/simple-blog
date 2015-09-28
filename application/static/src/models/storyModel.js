'use strict';

/**
 * Define the ENTRIES_LOADED event which this model emits
 */
namespace('models.events').ENTRIES_LOADED = 'StoryModel.ENTRIES_LOADED';

/**
 * Story Model
 *
 * Pulls most popular stories plus scrapes each story's target
 * url in order to retrieve embed information.
 */
var StoryModel = Class.extend({
  stories: [],
  events: null,
  $q: null,
  hackerNewsService: null,

  /**
   * Init class
   */
  init: function(Events, $q, HackerNewsService) {
    this.events = Events;
    this.$q = $q;
    this.hackerNewsService = HackerNewsService;
  },

  /**
   * Load the top stories filtered by read state
   */
  loadStories: function(page) {
    var deferred = this.$q.defer();
    var limit = 20;
    page = page > 1 ? page : 1;

    this.hackerNewsService.getTopStoryIds().then(function(data) {
      this.stories = data;

      this.events.notify(models.events.ENTRIES_LOADED);
      deferred.resolve(this.stories);

    }.bind(this));

    return deferred.promise;
  },

  /**
   * Get the list of stories
   */
  getStories: function() {
    return this.stories;
  },

  /**
   * Set a story as read/unread
   */
  setRead: function(story, val) {
    story.read = val;
    this.readMarkerModel.saveId(story.id, val);
  }

});

(function() {
  var StoryModelProvider = Class.extend({
    $get: function(Events, $q, HackerNewsService) {
      return new StoryModel(Events, $q, HackerNewsService);
    }
  });

  angular.module('story.StoryModel',[])
    .provider('StoryModel', StoryModelProvider);
}());
