var appRoot = require('app-root-path');
const scriptsFolder = appRoot + '/eahub/base/static/components/';
const Marker = require(`${scriptsFolder}/maps/marker.js`).default;
const Mocks = require('../helpers/mocks.js').default;

describe('Marker', function() {
  let marker, mapMock, profilesMock
  beforeEach(function() {
    mapMock = {
      google: Mocks.googleMock,
      type: 'groups',
      markerSettings: Mocks.markerSettingsMock
    }

  })
  afterEach(function() {
    mapMock = null
  })

  describe('constructor', function(){
    it('creates googleMarker whose label shows the number of profiles linked to marker', function() {
      marker = new Marker(mapMock, Mocks.londonLatLng, [Mocks.london1Mock, Mocks.london2Mock])

      expect(marker.googleMarker.label.text).toBe('2')
    })
    it('creates googleMarker whose icon is active if some profiles in it are active', function() {
      marker = new Marker(mapMock, Mocks.londonLatLng, [Mocks.london1Mock, Mocks.london2Mock])

      expect(marker.googleMarker.icon.url).not.toContain('inactive')
      expect(marker.googleMarker.icon.url).toContain('active')
    })
    it('creates googleMarker whose icon is active if map type is individuals', function() {
      mapMock.type = 'individuals'
      marker = new Marker(mapMock, Mocks.londonLatLng, [Mocks.london1Mock, Mocks.london2Mock])

      expect(marker.googleMarker.icon.url).not.toContain('inactive')
      expect(marker.googleMarker.icon.url).toContain('active')
    })
    it('creates googleMarker whose icon is inactive if all profiles in it are inactive', function() {
      marker = new Marker(mapMock, Mocks.londonLatLng, [Mocks.london2Mock])

      expect(marker.googleMarker.icon.url).toContain('inactive')
    })
  })
  describe('addDescription', function() {
    it('adds list of profiles to marker', function() {
      marker = new Marker(mapMock, Mocks.londonLatLng, [Mocks.london1Mock, Mocks.london2Mock])
      marker.addDescription()

      expect(marker.googleMarker.desc).toContain('London1')
      expect(marker.googleMarker.desc).toContain('London2')
    })
    it('adds links to profiles to marker', function() {
      marker = new Marker(mapMock, Mocks.londonLatLng, [Mocks.london1Mock, Mocks.london2Mock])
      marker.addDescription()

      expect(marker.googleMarker.desc).toContain('london-1')
      expect(marker.googleMarker.desc).toContain('london-2')
    })
    it('adds that groups is inactive to marker', function() {
      marker = new Marker(mapMock, Mocks.londonLatLng, [Mocks.london1Mock, Mocks.london2Mock])
      marker.addDescription()

      expect(marker.googleMarker.desc).toContain('London2 (inactive)')
    })
  })
})
