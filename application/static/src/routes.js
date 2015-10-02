'use strict';

app.config(function($stateProvider, $urlRouterProvider) {

  // For any unmatched url, redirect to /
  $urlRouterProvider.otherwise('/');

  // Now set up the states
  $stateProvider
    .state('about', {
      url: '/about',
      templateUrl: 'partials/about/about.html'
    })
    .state('create', {
      url: '/create',
      templateUrl: 'partials/create/create.html'
    })
    .state('home', {
      url: '/:page',
      params: {
        page: {value: '', squash: true}
      },
      templateUrl: 'partials/home/home.html',
      controller: HomeController
    });
});
