describe('Marker', function() {
  let marker, mapMock, profilesMock
  beforeEach(function() {
    mapMock = {
      google: googleMock,
      type: 'groups'
    }

  })
  afterEach(function() {
    mapMock = null
  })

  describe('constructor', function(){
    it('creates googleMarker whose label shows the number of profiles linked to marker', function() {
      marker = new Marker(mapMock, londonLatLng, [london1Mock, london2Mock])

      expect(marker.googleMarker.label.text).toBe('2')
    })
    it('creates googleMarker whose icon is active if some profiles in it are active', function() {
      marker = new Marker(mapMock, londonLatLng, [london1Mock, london2Mock])

      expect(marker.googleMarker.icon.url).not.toContain('inactive')
      expect(marker.googleMarker.icon.url).toContain('active')
    })
    it('creates googleMarker whose icon is active if map type is individuals', function() {
      mapMock.type = 'individuals'
      marker = new Marker(mapMock, londonLatLng, [london1Mock, london2Mock])

      expect(marker.googleMarker.icon.url).not.toContain('inactive')
      expect(marker.googleMarker.icon.url).toContain('active')
    })
    it('creates googleMarker whose icon is inactive if all profiles in it are inactive', function() {
      marker = new Marker(mapMock, londonLatLng, [london2Mock])

      expect(marker.googleMarker.icon.url).toContain('inactive')
    })
  })
  describe('addDescription', function() {
    it('adds list of profiles to marker', function() {
      marker = new Marker(mapMock, londonLatLng, [london1Mock, london2Mock])
      marker.addDescription()

      expect(marker.googleMarker.desc).toContain('London1')
      expect(marker.googleMarker.desc).toContain('London2')
    })
    it('adds links to profiles to marker', function() {
      marker = new Marker(mapMock, londonLatLng, [london1Mock, london2Mock])
      marker.addDescription()

      expect(marker.googleMarker.desc).toContain('london-1')
      expect(marker.googleMarker.desc).toContain('london-2')
    })
    it('adds that groups is inactive to marker', function() {
      marker = new Marker(mapMock, londonLatLng, [london1Mock, london2Mock])
      marker.addDescription()

      expect(marker.googleMarker.desc).toContain('London2 (inactive)')
    })
  })
})
