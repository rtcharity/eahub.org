var appRoot = require('app-root-path');
const scriptsFolder = appRoot + '/eahub/base/static/components/';
const Heatmap = require(`${scriptsFolder}/maps/heatmap.js`).default;
const LocationCluster = require(`${scriptsFolder}/maps/locationCluster.js`).default;
const LocationClusters = require(`${scriptsFolder}/maps/locationClusters.js`).default;
const Marker = require(`${scriptsFolder}/maps/marker.js`).default;
const Profile = require(`${scriptsFolder}/maps/profile.js`).default;

const Mocks = require('../helpers/mocks.js').default;

describe('Heatmap', function() {
  let mapIndividuals, mapGroups, mapModules, isIE
  beforeEach(function() {
    isIE = false
    mapModules = {
      locationCluster: LocationCluster,
      locationClusters: LocationClusters,
      marker: Marker,
      profile: Profile
    }
    mapIndividuals = new Heatmap('individuals', Mocks.locationsMock, mapModules, Mocks.externalModulesMock, Mocks.htmlElementsMock, isIE)
    mapGroups = new Heatmap('groups', Mocks.locationsMock, mapModules, Mocks.externalModulesMock, Mocks.htmlElementsMock, isIE)
  })
  afterEach(function() {
    mapIndividuals = null
    mapGroups = null
  })
  describe('setup', function() {
    it('renders groups if type is groups', function() {
      mapGroups.setup()
      mapGroups.locationClusters.list.forEach(function(cluster) {
        cluster.profiles.forEach(function(profile) {
          expect(profile.type).toBe('groups')
        })
      })
    })
    it('renders individuals if type is individuals', function() {
      mapIndividuals.setup()

      mapIndividuals.locationClusters.list.forEach(function(cluster) {
        cluster.profiles.forEach(function(profile) {
          expect(profile.type).toBe('individuals')
        })
      })
    })
    it('sets the selector to individuals if queryStringMap is individuals', function() {
      mapIndividuals.setup()

      expect(mapIndividuals.selectorInd.checked).toBe(true)
    })
    it('sets the selector to groups if queryStringMap is groups', function() {
      mapGroups.setup()

      expect(mapGroups.selectorGroups.checked).toBe(true)
    })
  })
  describe('render', function() {
    var klaipedaCluster, londonCluster, klaipedaMarker, londonMarker

    beforeEach(function() {
      mapGroups.setup()
      mapIndividuals.setup()
      klaipedaMarker = mapGroups.locationClusters.list.filter(cluster => cluster.location.lat == Mocks.klaipedaLatLng.lat && cluster.location.lng == Mocks.klaipedaLatLng.lng)[0].markers[0]
      londonMarker = mapIndividuals.locationClusters.list.filter(cluster => cluster.location.lat == Mocks.londonLatLng.lat && cluster.location.lng == Mocks.londonLatLng.lng)[0].markers[0]
    })
    afterEach(function() {
      mapGroups, mapIndividuals, klaipedaMarker, londonMarker = null
    })
    it('renders location clusters with number of profiles in that location', function() {
      expect(klaipedaMarker.googleMarker.label.text).toEqual('2')
    })
    it('does not count private profiles in markers where number of private profiles < kAnonymity', function() {
      expect(londonMarker.googleMarker.label.text).toEqual('1')
    })
    it('adds the list of all public profiles in a location in its marker', function() {
      expect(klaipedaMarker.googleMarker.desc).toContain('klaipeda-1')
      expect(klaipedaMarker.googleMarker.desc).toContain('klaipeda-2')
    })
    it('does not add private profiles to list in markers', function() {
      expect(londonMarker.googleMarker.desc).not.toContain('<ul>')
    })
  })
})
