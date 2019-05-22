describe("createProfile", function() {
  
  it("returns anonymous profile with no path if no label and path given", function() {
    var locationAnonymousMock = {lat: 50, lng: 0}

    expect(map.createProfile(locationAnonymousMock).anonymous).toBe(true)
    expect(map.createProfile(locationAnonymousMock).path).toBeUndefined()
  })
  it("returns profile with path and label if given", function() {
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
