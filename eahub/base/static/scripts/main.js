import $ from "jquery";
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.css';
import './bootstrap-multiselect/bootstrap-multiselect.js';
import '../styles/bootstrap-multiselect.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import '@fortawesome/fontawesome-free/js/all.min.js';
import '../styles/fonts/open-sans.css';
import '../styles/main.css';

import MarkerClusterer from '@google/markerclusterer';
import Navbar from './navbar.js';
import MultiselectForms from './multiselect-forms.js';
import GroupPageActions from './group-page-actions.js'
import ProfileEditImage from './profile-edit-image.js'
import Tables from './tables.js';
import Heatmap from './maps/heatmap.js';
import LocationCluster from './maps/locationCluster.js';
import LocationClusters from './maps/locationClusters.js';
import Marker from './maps/marker.js';
import Profile from './maps/profile.js';

$(document).ready(function () {
  const tables = new Tables($('#datatable-profiles'), $('#datatable-groups'));
  tables.applySearchFunctionalityToAllTables();

  const navbar = new Navbar($('#burger-btn'), $('#navbar'));
  navbar.toggleMenuOnClick();
  navbar.disappearMenuOnMovingCursorAway();

  const selectorsWithOldStyle = [
    $('#id_local_groups'),
    $('#id_available_as_speaker'),
    $('#id_open_to_job_offers'),
    $('#id_available_to_volunteer')
  ]

  // const multiselectFormHtmlElements = $('.multiselect-form')
  // const multiselectForm = new MultiselectForms(multiselectFormHtmlElements, selectorsWithOldStyle, 10);
  // multiselectForm.applySettings();

  let claimGroupHtmlElements = {
    toggle_btn: $('#claim_group_toggle'),
    confirm_field: $('#claim_group_confirm_field'),
    togglers: $('#claim_group_toggler')
  }

  let reportGroupHtmlElements = {
    toggle_btn: $('#report_group_inactive_toggle'),
    confirm_field: $('#report_group_inactive_confirm_field'),
    togglers: $('#report_group_inactive_toggler')
  }

  const groupPageActions = new GroupPageActions([claimGroupHtmlElements, reportGroupHtmlElements]);
  groupPageActions.toggleEachElementOnClick();

  const imageHtmlElement = $('#id_image');
  const imageChangeHtmlElements = {
    container: $('#image-change'),
    toggle: $('#image-change-toggle')
  }
  const imageClearHtmlElements = {
    container: $('#image-clear'),
    checkbox: $('#image-clear_id')
  }
  const profileEditImage = new ProfileEditImage(imageHtmlElement, imageChangeHtmlElements, imageClearHtmlElements);
  profileEditImage.toggleImageChangeOnClick();
  profileEditImage.removeImageClearOnInput();
});

window.initHeatmapFull = function initHeatmapFull(queryStringMap) {
  var mapParams = getMapParams();
  var mapLocations = JSON.parse(document.getElementById('map-locations').textContent);
  var newMap = new Heatmap(queryStringMap, mapLocations, mapParams.mapModules, mapParams.externalModules, mapParams.htmlElements, isIE)
  newMap.setup();
}

window.initHeatmapList = function initHeatmapList(queryStringMap) {
  var mapParams = getMapParams();
  var mapLocations = JSON.parse(document.getElementById('map-locations').textContent);
  var newMap = new Heatmap(queryStringMap, mapLocations, mapParams.mapModules, mapParams.externalModules, mapParams.htmlElements, isIE);
  newMap.render(mapLocations.profiles, mapLocations.private_profiles);
}

window.initHeatmapProfile = function initHeatmapProfile(mapLocations, htmlElements) {
  var mapParams = getMapParams();
  mapParams.htmlElements = htmlElements;
  var newMap = new Heatmap(undefined, mapLocations, mapParams.mapModules, mapParams.externalModules, mapParams.htmlElements, isIE);
  newMap.renderProfilePageMap();
}

function getMapParams() {
  var mapSelectorInd = document.getElementById('map_selector_ind');
  var mapSelectorGroups = document.getElementById('map_selector_groups');
  var mapElement = document.getElementById('map')
  var htmlElements = {
    selectorInd: mapSelectorInd === undefined ? null : mapSelectorInd,
    selectorGroups: mapSelectorGroups === undefined ? null : mapSelectorGroups,
    map: mapElement === undefined ? null : mapElement,
  }
  var mapModules = {
    locationCluster: LocationCluster,
    locationClusters: LocationClusters,
    marker: Marker,
    profile: Profile,
  }
  var externalModules = {
    google: google,
    markerClusterer: MarkerClusterer
  }
  return {mapModules, externalModules, htmlElements}
}
