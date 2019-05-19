describe("Heatmap Module", function() {
  var queryStringMap = 'individuals'
  var map_locations = []
  var mapSelectorInd = {}
  var mapSelectorGroups = {}
  var map = new mapObj(queryStringMap,map_locations,mapSelectorInd,mapSelectorGroups)
  console.log(map)
  it("has setup function", function() {
    var setup = map.setup
    expect(setup).not.toBe(undefined);
  });
  it("setup function calls render", function() {

    var spy = spyOn(map, 'render')

    map.setup(queryStringMap, map_locations, mapSelectorInd, mapSelectorGroups)

    expect(spy).toHaveBeenCalled()
  })
});
