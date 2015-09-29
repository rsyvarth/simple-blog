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
  storyService: null,

  /**
   * Init class
   */
  init: function(Events, $q, StoryService) {
    this.events = Events;
    this.$q = $q;
    this.storyService = StoryService;
  },

  /**
   * Load the top stories filtered by read state
   */
  loadStories: function(cursor) {
    var deferred = this.$q.defer();

    this.storyService.getStories(cursor).then(function(data) {
      var i = 0;
      for(; i < data.entries.length; i++) {
        data.entries[i].timestamp = moment.utc(data.entries[i].timestamp).unix();
      }
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
    $get: function(Events, $q, StoryService) {
      return new StoryModel(Events, $q, StoryService);
    }
  });

  angular.module('story.StoryModel',[])
    .provider('StoryModel', StoryModelProvider);
}());
