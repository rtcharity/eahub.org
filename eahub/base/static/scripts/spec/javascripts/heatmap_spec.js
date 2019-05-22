describe("Heatmap Module", function() {
  var queryStringMap, profileMock, privateProfileMock, groupMock, isIEMock,
  locationsMock, selectorIndMock, selectorGroupsMock,
  mapElementMock, genericFunctionMock, documentMock, googleMock,
  markerClustererMock, map, clusterMock, clusterMockOther, locationMock, locationClustersMock

  var profileClass = class {
    constructor(location, mapType) {
      this.label = location.label != undefined ? location.label : undefined
      this.anonymous = location.label != undefined ? false : true
      this.path = location.path != undefined ? location.path : undefined
      this.active = mapType == 'groups' ? true : undefined
    }
  }

  beforeEach(function() {
    queryStringMap = 'individuals'
    profileMock = jasmine.createSpy('profileMock')
    privateProfileMock = jasmine.createSpy('privateProfileMock')
    groupMock = jasmine.createSpy('groupMock')
    isIEMock = jasmine.createSpy('isIEMock')
    locationMock = {lat: 50, lng: 0, path: "/path", label: "user"}
    clusterMock = {lat: 50, lng: 0, profiles: [profileMock, privateProfileMock]}
    clusterMockOther = {lat: 50, lng: 20, profiles: [profileMock, privateProfileMock]}
    locationClustersMock = [clusterMock, clusterMockOther]
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
    map = new mapObj(queryStringMap,locationsMock,selectorIndMock,selectorGroupsMock, googleMock, markerClustererMock, documentMock, isIEMock, profileClass)
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
    it("returns true if index is less than length of location clusters", function() {
      expect(map.isinSameLocationAsOneOf(locationClustersMock, 1)).toBe(true)
    })
    it("returns false if index is more or equal than length of location clusters", function() {
      expect(map.isinSameLocationAsOneOf(locationClustersMock, 2)).toBe(false)
    })
  })

  describe("countMarkersAt", function() {
    it("returns 2 for location with 2 profiles in its cluster", function() {
      expect(map.countMarkersAt(locationMock, locationClustersMock)).toBe(2)
    })
  })


});
