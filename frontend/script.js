angular.module('eaHubApp', ['ngRoute']);

angular.module('eaHubApp').service('users', function($http) {
  const users = this;

  users.get = () =>
    $http({
      method: 'GET',
      url: `../api/users`
    });
});

angular.module('eaHubApp').service('groups', function($http) {
  const groups = this;

  groups.get = () =>
    $http({
      method: 'GET',
      url: `../api/groups`
    });
});

angular.module('eaHubApp').config(($routeProvider) => {
  $routeProvider.when('/users', {
    template: '<users></users>'
  })
  $routeProvider.when('/groups', {
    template: '<groups></groups>'
  })
  .otherwise({
    redirectTo: '/groups'
  });
});

angular.module('eaHubApp').component('users', {
  template: `<h2>hey users</h2>
  <ul>
    <li ng-repeat="user in $ctrl.list">{{user.id}} {{user.name}}</li>
  </ul>`,
  controller: function(users) {
    const $ctrl = this;

    $ctrl.$onInit = () => {
      users.get((list) => {
        $ctrl.list = list;
      });
    };
  }
})

angular.module('eaHubApp').component('groups', {
  template: `<h2>hey groups</h2>
  <ul>
    <li ng-repeat="group in $ctrl.list">{{group.id}} {{group.name}}</li>
  </ul>
  `,
  controller: function(groups) {
    const $ctrl = this;

    $ctrl.$onInit = () => {
      groups.get((list) => {
        $ctrl.list = list;
      });
    };
  }
})
