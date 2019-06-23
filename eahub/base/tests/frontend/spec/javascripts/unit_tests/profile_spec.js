var appRoot = require('app-root-path');
const scriptsFolder = appRoot + '/eahub/base/static/scripts/';
const Profile = require(`${scriptsFolder}/maps/profile.js`).default;

describe("Profile", function() {
  describe("constructor", function() {
    let locationMock, type
    beforeEach(function() {
      locationMock = {}
      type = ''
    })
    afterEach(function() {
      locationMock = {}
      type = ''
    })
    it("creates an anonymous profile where label is undefined and type is not groups", function() {
      locationMock.label = undefined
      type = 'individuals'

      let profile = new Profile(locationMock, type)

      expect(profile.anonymous).toBe(true)
    })

    it("does not create an anonymous group where type is groups", function() {
      locationMock.label = undefined
      type = 'groups'

      let profile = new Profile(locationMock, type)

      expect(profile.anonymous).toBe(false)
    })

    it('sets active property only if type is groups', function() {
      type = 'individuals'
      locationMock.active = true

      let profile = new Profile(locationMock, type)

      expect(profile.active).not.toBeDefined()
    })
  })
})
