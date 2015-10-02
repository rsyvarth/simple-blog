'use strict';

var app = angular.module('app', [
  'events',

  'storage.persistentStorageService',

  'storyList',
  'story.StoryModel',
  'story.StoryService',

  'loginButton',
  'subscribeButton',
  'user.UserModel',
  'user.UserService',

  'createForm',

  'ui.router',
  'pascalprecht.translate',
  'angularMoment'
]);

// HTML5 mode allows for routes without the # on modern browsers
app.config(function($locationProvider) {
  $locationProvider.html5Mode(true);
});

// Enabled default translation
app.config(['$translateProvider', function($translateProvider) {
  $translateProvider
    .translations('en', translations) //translations is set in lang/en/lang.js
    .preferredLanguage('en')
    .useSanitizeValueStrategy('escape');
}]);

// Register Material Design Light components on view change
app.run(function($rootScope, $timeout) {
  $rootScope.$on('$viewContentLoaded', function() {
    $timeout(function() {
      componentHandler.upgradeAllRegistered();
    });
  });
});
