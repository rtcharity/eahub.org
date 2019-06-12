describe('LocationClusters', function() {
  let locationClustersMock, mapMock, allLocationsMock, londonLatLng, klaipedaLatLng
  beforeEach(function() {
    mapMock = {
      mapModules: {
        locationCluster: LocationCluster,
        profile: Profile
      }
    }
    londonLatLng = {lat: 50, lng: 0}
    klaipedaLatLng = {lat: 55, lng: 22}
    locationLondon1Mock = {lat: londonLatLng.lat, lng: londonLatLng.lng, label: 'London1'}
    locationLondon2Mock = {lat: londonLatLng.lat, lng: londonLatLng.lng, label: 'London2'}
    locationKlaipeda1Mock = {lat: klaipedaLatLng.lat, lng: klaipedaLatLng.lng, label: 'Klaipeda1'}
    allLocationsMock = [locationLondon1Mock, locationLondon2Mock, locationKlaipeda1Mock]

    locationClusters = new LocationClusters(allLocationsMock, mapMock)
  })
  afterEach(function() {
    locationClusters = null
  })
  describe('constructor', function() {
    it('creates a list of clusters of locations with same lat and lng', function() {
      expect(locationClusters.list.length).toBe(2)

      expect(locationClusters.list[0].location).toEqual(londonLatLng)
      expect(locationClusters.list[1].location).toEqual(klaipedaLatLng)

      expect(locationClusters.list[0].profiles.length).toEqual(2)
      expect(locationClusters.list[1].profiles.length).toEqual(1)

    })
  })
  describe('add', function() {
    it('new cluster to list of clusters', function() {
      let windenLatLng = {lat: 50, lng: 10}
      let clusterWindenMock = { location: windenLatLng }
      locationClusters.add(clusterWindenMock)

      expect(locationClusters.list.length).toEqual(3)
      expect(locationClusters.list[2].location).toEqual(windenLatLng)
    })
    it('update existing cluster in list if location is the same', function() {
      let clusterKlaipedaMock = { location: klaipedaLatLng, profiles: [{label: 'Klaipeda1'}, {label: 'Klaipeda2'}]}
      locationClusters.add(clusterKlaipedaMock)
      expect(locationClusters.list.length).toEqual(2)
      expect(locationClusters.list[1].profiles[1].label).toBe('Klaipeda2')
    })
  })
})
