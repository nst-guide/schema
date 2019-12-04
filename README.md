# Schema

This repository holds JSON Schemas to validate each of the tables of the project.

The idea is that with small wrappers written in JS and Python, this can be an
importable package that is used any time data is being updated.

This is a work in progress!

## Tables

Below is pseudocode/TypeScript for the schemas. Actual parsing happens in the
JSON schema files, anything below is unofficial and just for documentation
purposes.

I'm planning to use Parse Server, an open source backend as a service, for my
backend. This has a `GeoPoint` type. Consider `GeoPoint` to be a standard object
with `latitude` and `longitude` keys. Parse adds `__type: "GeoPoint"`, but this
is not required if working outside Parse.

```ts
interface GeoPoint {
    __type?: string
    latitude: number,
    longitude: number,
}
```

For now, I'll say a `Geometry` is always a valid GeoJSON string. (Encoded as a
string, not an object).
```ts
type Geometry: string
```

### Town

Rows should be unique among towns. A "town" can include resupply areas that are
not generally considered towns. For example, a lodge in Oregon that's just off
the trail but remote could be considered its own Town.

```ts
interface Town {
    // Unique identifier for town
    id: number,
    // Common name for town
    name: string,
    // Geographic centroid of town. I think this probably is meant to be more of
    // a "representative point" in Shapely's parlance. A centroid may be outside
    // of a polygon; it would be nice if the centroid argument is always within
    // the Town, but this is not required.
    centroid: GeoPoint,
    // Actual geometry of town. While centroid may be used when zoomed out,
    // geometry should be a more accurate geometric representation of the town.
    geometry: Geometry,
    // trails that this Town is a part of. I.e. [PCT]
    trails: string[],
}
```

### TownWaypoint

```ts
interface TownWaypoint {
    id: number,
    // Reference to Town table
    townId: number,
    name: string,
    // description
    desc?: string,
    // information about the type of waypoint this is
    type: TownWaypointType
    subtype: TownWaypointSubtype
    // location: most town waypoints will be Points
    geopoint: GeoPoint
    // Optionally, more accurate waypoint
    geometry?: Geometry
    // object that holds OSM information
    osm: TownOSM,
    // attributes that are not pinned to OSM
    attributes: TownAttributes,
}
// TODO figure out waypoint type and subtype
enum TownWaypointType {
    Food,
    Lodging,
    Camping,
    ...
}
enum TownWaypointSubtype {
    FastFood
    Restaurant
    Bar
    Hotel
    Motel
    Camping
    ...
}
interface TownOSM {
    nodeId?: number,
    wayId?: number,
    relationId?: number,
    // showers, toilets and laundry are values within the amenity and shop keys
    amenity?: string,
    shop?: string,
    // Opening hours should conform to OSM opening hours standard. Parsers:
    // Python: https://github.com/rezemika/humanized_opening_hours
    // JS: https://github.com/opening-hours/opening_hours.js
    opening_hours?: string,
    phone?: string,
    website?: string,
    // internet_access==wlan
    internet_access?: boolean,
    internet_access_fee?: boolean,
    toilets_disposal?: string,
    drinking_water?: boolean,
}
interface TownAttributes {
    wifi?: boolean,
    phone?: string,
    website?: string,
    // power outlets
    power?: boolean,
    shower?: boolean,
    showerFee?: string,
    laundry?: boolean,
    laundryFee?: string,
    toilets?: boolean,
    toiletsFlush?: boolean,
}
```

### Trail

An overall, named hiking trail, like the Pacific Crest Trail, or Appalachian Trail.

```ts
interface Trail {
    id: number,
    name: string,
    desc: string,
    // Link to TrailSection
    trailSections: string[]
}
```

### TrailSection

A smaller part of a larger Trail.

```ts
interface TrailSection {
    id: number,
    alternate: boolean,
}
```

### TrailWaypoint

Waypoints that are part of a TrailSection and are trail-focused. A resupply
location should be a TownWaypoint.

```ts
interface TrailWaypoint {
    id: number,
    name?: string,
    desc?: string,
    type: TrailWaypointType
    subtype: TrailWaypointSubtype
}
enum TrailWaypointType {

}
enum TrailWaypointSubtype {

}
```


## To Do

- How to name tables so that they're easiest to download for offline usage in Parse. I think Parse generally downloads an entire table. Should all tables be prefixed by `PCT_`?
- strings or numbers for identifiers
