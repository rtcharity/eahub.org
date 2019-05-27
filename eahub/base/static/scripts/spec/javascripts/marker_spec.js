describe('Marker', function() {
  let marker, mapMock, googleMarkerMock, googleSizeMock, activeProfileMock,
      inactiveProfileMock, profilesMock, locationMock


  beforeEach(function() {
    googleMarkerMock = class {
      constructor(props) {
        this.label = props.label
        this.setIcon = function(icon) {
          this.icon = icon
        }
      }
    }
    googleSizeMock = class {
      constructor(size1, size2) {
        this.size1 = size1,
        this.size2 = size2
      }
    }
    mapMock = {
      google: {
        maps: {
          Marker: googleMarkerMock,
          Size: googleSizeMock
        }
      },
      type: 'groups'
    }
    activeProfileMock = {active: true}
    inactiveProfileMock = {active: false}
    locationMock = {lat: 50, lng: 0}
  })
  afterEach(function() {
    mapMock = null
  })

  describe('constructor', function(){
    it('creates googleMarker whose label shows the number of profiles linked to marker', function() {
      profilesMock = [activeProfileMock, activeProfileMock]
      marker = new Marker(mapMock, locationMock, profilesMock)

      expect(marker.googleMarker.label.text).toBe('2')
    })
    it('creates googleMarker whose icon is active if some profiles in it are active', function() {
      profilesMock = [activeProfileMock, activeProfileMock]
      marker = new Marker(mapMock, locationMock, profilesMock)

      expect(marker.googleMarker.icon.url).not.toContain('inactive')
      expect(marker.googleMarker.icon.url).toContain('active')
    })
    it('creates googleMarker whose icon is active if map type is individuals', function() {
      profilesMock = [activeProfileMock, activeProfileMock]
      mapMock.type = 'individuals'
      marker = new Marker(mapMock, locationMock, profilesMock)

      expect(marker.googleMarker.icon.url).not.toContain('inactive')
      expect(marker.googleMarker.icon.url).toContain('active')
    })
    it('creates googleMarker whose icon is inactive if all profiles in it are inactive', function() {
      profilesMock = [inactiveProfileMock, inactiveProfileMock]
      marker = new Marker(mapMock, locationMock, profilesMock)

      expect(marker.googleMarker.icon.url).toContain('inactive')
    })
  })
})
