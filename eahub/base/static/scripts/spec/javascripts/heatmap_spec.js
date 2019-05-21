describe("Heatmap Module", function() {
  var queryStringMap, profileMock, privateProfileMock, groupMock, isIEMock,
  locationsMock, selectorIndMock, selectorGroupsMock,
  mapElementMock, genericFunctionMock, documentMock, googleMock,
  markerClustererMock, map, clusterMock, clusterMockOther

  beforeEach(function() {
    queryStringMap = 'individuals'
    profileMock = jasmine.createSpy('profileMock')
    privateProfileMock = jasmine.createSpy('privateProfileMock')
    groupMock = jasmine.createSpy('groupMock')
    isIEMock = jasmine.createSpy('isIEMock')
    clusterMock = {lat: 50, lng: 0}
    clusterMockOther = {lat: 50, lng: 20}
    locationsMock = {
      profiles: [profileMock],
      private_profiles: [privateProfileMock],
      groups: [groupMock]
    }
    selectorIndMock = { checked: false }
    selectorGroupsMock = { checked: false }
    mapElementMock = 'mapElementMock'
    genericFunctionMock = function() {
      return null
    }
    documentMock = {
      getElementById: function() { return mapElementMock }
    }
    googleMock = {
      maps: {
        LatLng: function(lat, lng) {
          return {lat, lng}
        },
        InfoWindow: genericFunctionMock,
        Map: function(mapElement, mapOptions) {
          return {mapElement, mapOptions}
        },
        event: {
          addListener: genericFunctionMock
        },
        Marker: function() {
          return {
            setIcon: genericFunctionMock,
            addListener: genericFunctionMock,
            setMap: genericFunctionMock
          }
        },
        Size: genericFunctionMock
      }
    }
    markerClustererMock = function(map, markers, properties) {
      return 0
    }
    map = new mapObj(queryStringMap,locationsMock,selectorIndMock,selectorGroupsMock, googleMock, markerClustererMock, documentMock, isIEMock)
  })

  describe("setup function", function() {
    it("renders map set in type", function() {
      var spy = spyOn(map, 'render')

      map.setup()

      expect(spy).toHaveBeenCalledWith(locationsMock.profiles, locationsMock.private_profiles)
    })

    it("sets checked property of map toggler", function() {
      map.setup()

      expect(map.selectorInd.checked).toBe(true)
    })

    it("adds functionality to map togglers", function() {
      var spy = spyOn(map, 'toggle')

      map.setup()

      expect(spy).toHaveBeenCalled()
    })
  })

  describe("render function", function() {
    it("creates location clusters", function() {
      var spy = spyOn(map, 'createLocationClusters').and.callThrough()
      map.render(map.locations.profiles, map.locations.private_profiles)
      expect(spy).toHaveBeenCalled()
    })
    it("creates map", function() {
      var spy = spyOn(map, 'createMap')
      map.render(map.locations.profiles, map.locations.private_profiles)
      expect(spy).toHaveBeenCalled()
    })
  })

  describe("createMap function", function() {
    it("returns map", function() {
      var actual = map.createMap()

      expect(actual.mapElement).toBe(mapElementMock)
    })
  })

  describe("isSameLocation", function() {
    var profileMock

    beforeEach(function() {
      profileMock = {lat: 50, lng: 0}
    })

    it("returns true if profile is in same location as cluster", function() {
      expect(map.isSameLocation(profileMock, clusterMock)).toBe(true)
    })

    it("returns false if profile is in different location than cluster", function() {
      expect(map.isSameLocation(profileMock, clusterMockOther)).toBe(false)
    })
  })

  describe("isinSameLocationAsOneOf", function() {
    var locationClustersMock = [clusterMock, clusterMockOther]
    it("returns true if index is less than length of location clusters", function() {
      expect(map.isinSameLocationAsOneOf(locationClustersMock, 1)).toBe(true)
    })
    it("returns false if index is more or equal than length of location clusters", function() {
      expect(map.isinSameLocationAsOneOf(locationClustersMock, 2)).toBe(false)
    })
  })

  describe("createProfile", function() {
    it("returns anonymous profile with no path if no label and path given", function() {
      var locationAnonymousMock = {lat: 50, lng: 0}

      expect(map.createProfile(locationAnonymousMock).anonymous).toBe(true)
      expect(map.createProfile(locationAnonymousMock).path).toBeUndefined()
    })
    it("returns profile with path and label if given", function() {
      var locationMock = {lat: 50, lng: 0, path: "/path", label: "user"}

      expect(map.createProfile(locationMock).path).toBe("/path")
      expect(map.createProfile(locationMock).label).toBe("user")
      expect(map.createProfile(locationMock).anonymous).toBeUndefined()
    })
    it("adds activity status to profile if map type is group", function() {
      map.type = "groups"
      var locationGroupMock = {lat: 50, lng: 0, active: true}

      expect(map.createProfile(locationGroupMock).active).toBe(true)
    })
  })


});
