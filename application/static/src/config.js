'use strict';

window.config = {
  key: 'val',
  baseUrl: ''
};

if(window.location.hostname === 'localhost') {
    config.baseUrl = 'http://localhost:8080/';
}
