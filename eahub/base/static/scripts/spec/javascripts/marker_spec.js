describe('Marker', function() {
  let marker, mapMock, profilesMock, locationMock
  beforeEach(function() {
    mapMock = {
      google: googleMock,
      type: 'groups'
    }
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
