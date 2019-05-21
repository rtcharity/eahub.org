describe("Heatmap Module", function() {
  var query_string_map, mockProfile, mockPrivateProfile, mockGroup, mockIsIE,
  map_locations_mock, map_selector_ind_mock, map_selector_groups_mock,
  mockMapElement, mockGenericFunction, documentMock, googleMock,
  markerClustererMock, map

  beforeEach(function() {
    query_string_map = 'individuals'
    mockProfile = jasmine.createSpy('mockProfile')
    mockPrivateProfile = jasmine.createSpy('mockPrivateProfile')
    mockGroup = jasmine.createSpy('mockGroup')
    mockIsIE = jasmine.createSpy('mockIsIE')
    map_locations_mock = {
      profiles: [mockProfile],
      private_profiles: [mockPrivateProfile],
      groups: [mockGroup]
    }
    map_selector_ind_mock = { checked: false }
    map_selector_groups_mock = { checked: false }
    mockMapElement = 'mockMapElement'
    mockGenericFunction = function() {
      return null
    }
    documentMock = {
      getElementById: function() { return mockMapElement }
    }
    googleMock = {
      maps: {
        LatLng: function(lat, lng) {
          return {lat, lng}
        },
        InfoWindow: mockGenericFunction,
        Map: function(mapElement, mapOptions) {
          return {mapElement, mapOptions}
        },
        event: {
          addListener: mockGenericFunction
        },
        Marker: function() {
          return {
            setIcon: mockGenericFunction,
            addListener: mockGenericFunction,
            setMap: mockGenericFunction
          }
        },
        Size: mockGenericFunction
      }
    }
    markerClustererMock = function(map, markers, properties) {
      return 0
    }
    map = new mapObj(query_string_map,map_locations_mock,map_selector_ind_mock,map_selector_groups_mock, googleMock, markerClustererMock, documentMock, mockIsIE)
  })

  describe("setup function", function() {
    it("renders map set in map_type", function() {
      var spy = spyOn(map, 'render')

      map.setup()

      expect(spy).toHaveBeenCalledWith(map_locations_mock.profiles, map_locations_mock.private_profiles)
    })

    it("sets checked property of map toggler", function() {
      map.setup()

      expect(map.map_selector_ind.checked).toBe(true)
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
      map.render(map.map_locations.profiles, map.map_locations.private_profiles)
      expect(spy).toHaveBeenCalled()
    })
    it("creates map", function() {
      var spy = spyOn(map, 'createMap')
      map.render(map.map_locations.profiles, map.map_locations.private_profiles)
      expect(spy).toHaveBeenCalled()
    })
  })

  describe("createMap function", function() {
    it("returns map", function() {
      var actual = map.createMap()

      expect(actual.mapElement).toBe(mockMapElement)
    })
  })

  describe("isSameLocation", function() {
    var profileMock

    beforeEach(function() {
      profileMock = {lat: 50, lng: 0}
    })

    it("returns true if profile is in same location as cluster", function() {
      var clusterMock = {lat: 50, lng: 0}
      expect(map.isSameLocation(profileMock, clusterMock)).toBe(true)
    })

    it("returns false if profile is in different location than cluster", function() {
      var clusterMockOther = {lat: 50, lng: 20}
      expect(map.isSameLocation(profileMock, clusterMockOther)).toBe(false)
    })
  })


});
