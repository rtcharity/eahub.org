describe('LocationCluster', function() {
  let locationCluster, locationMock, mapMock, profileMock, profileClassMock, markerMock, markerClassMock, spyOnGoogleMarker
  beforeEach(function() {
    locationMock = {lat: 0, lng: 50}
    profileMock = 'profileMock'
    profilesMock = [profileMock]
    profileClassMock = class ProfileClassMock {
      constructor(location, type) {
        this.location = location
        this.type = type
      }
    }
    spyOnGoogleMarker = jasmine.createSpy('googleMarker_setMap')
    markerClassMock = class MarkerClassMock {
      constructor(mapMock, locationMock, profilesMock, z) {
        this.location = locationMock
        this.googleMarker = {
          setMap: spyOnGoogleMarker
        }
        this.z = z
      }
    }
    mapMock = {
      type: 'individuals',
      mapModules: {
        profile: profileClassMock,
        marker: markerClassMock
      }
    }
    locationCluster = new LocationCluster(locationMock, mapMock)
  })
  afterEach(function() {
    locationCluster = null
  })
  describe('addProfile', function() {
    it('adds profile to list of profiles', function() {
      locationCluster.addProfile(locationMock)

      expect(locationCluster.profiles[0].type).toBe('individuals')
      expect(locationCluster.profiles[0].location).toEqual(locationMock)
    })
  })
  describe('addMarker', function() {
    it('adds profile to list of profiles', function() {
      locationCluster.addMarker()

      expect(locationCluster.markers[0].location).toEqual(locationMock)
    })
  })
  describe('addDummyMarkers', function() {
    let ten_profiles
    beforeEach(function() {
      ten_profiles = [1,2,3,4,5,6,7,8,9,10]
      locationCluster.profiles = ten_profiles
      locationCluster.addMarker()
      locationCluster.addDummyMarkers(1)
    })
    afterEach(function() {
      locationCluster.profiles = []
    })
    it('adds as many dummy markers so that there are as many markers as profiles', function() {
      expect(locationCluster.markers.length).toBe(10)
    })
    it('calls setMap on googleMarker', function() {
      expect(spyOnGoogleMarker).toHaveBeenCalled()
    })
    it('gives dummy Markers z-index of 0 or below', function() {
      expect(locationCluster.markers[1].z).toBeLessThan(1)
      expect(locationCluster.markers[9].z).toBeLessThan(1)
    })
  })
})
