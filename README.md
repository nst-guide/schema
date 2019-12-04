# Schema

This repository holds JSON Schemas to validate each of the tables of the project.

The idea is that with small wrappers written in JS and Python, this can be an
importable package that is used any time data is being updated.

This schema is for all data that will be held in the Parse Server/MongoDB
database. Not all data will be held here: rather, only data that is expected to
have frequent updates _and_ have two-way synchronization.

For example, a weather forecast layer does not need to be in here, because the
data is always going from server to client, and old data can be deleted. It
should be simple enough for this kind of data to check timestamps on the server,
and just automatically redownload if available during the syncing process.

This is a work in progress!

## Tables

Below is pseudocode/TypeScript for the schemas. Actual parsing happens in the
JSON schema files, anything below is unofficial and just for documentation
purposes.

### General types

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
type Geometry = string;
```

Comments will be permitted on many types of waypoints. Let's define the default
feedback as just an array of comments.
```ts
interface DefaultFeedback {
    comments: Comment[]
}
interface Comment {
    userId: string,
    body: string,
    // true == "northbound", where northbound is usually defined as south to
    // north, but could be defined as the "standard" way for an east-west facing
    // trail, like the Colorado Trail.
    direction?: boolean,
    date: Date,
}
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
    // Type of town
    townType: TownType,
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
    feedback: TownFeedback,
}
enum TownType {
    City
    Resort
}
interface TownFeedback {
    comments: Comments[]
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
    osm: TownWaypointOSM,
    // attributes that are not pinned to OSM
    attributes: TownWaypointAttributes,
    feedback: TownWaypointFeedback,
}
// TODO figure out waypoint type and subtype
enum TownWaypointType {
    Food,
    Lodging,
    Finance,
    Store,
    Medical,
    ...
}
type TownWaypointSubtype = FoodSubtype || LodgingSubtype || FinanceSubtype || StoreSubtype || MedicalSubtype;
enum FoodSubtype {
    FastFood,
    Cafe,
    Restaurant,
    Bar,
}
enum LodgingSubtype {
    Hotel,
    Motel,
    Camping,
}
enum FinanceSubtype {
    ATM,
    Bank,
}
enum StoreSubtype {
    OutdoorsStore,
    Grocery,
}
enum MedicalSubtype {
    Hospital,
    Pharmacy
}
interface TownWaypointOSM {
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
interface TownWaypointAttributes {
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
    acceptsResupply?: boolean
    acceptsResupplyFee?: string,
    acceptsResupplyProvider?: ResupplyProvider,
    acceptsResupplyAddress?: ResupplyAddress[],
    sendsResupply?: boolean,
    sendsResupplyProvider?: ResupplyProvider,
}
interface ResupplyProvider {
    ups?: boolean,
    usps?: boolean,
    fedex?: boolean,
}
interface ResupplyAddress {
    // either ups, usps, fedex
    provider: string[],
    address: Address,
}
interface Address {
    housenumber?: string,
    // comparable to address line 2
    flats?: string,
    street?: string,
    postcode?: string,
    city?: string,
    state?: string,
}
interface TownWaypointFeedback extends DefaultFeedback {
    upvotes: number,
    downvotes: number,
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
    type: TrailWaypointType,
    subtype: TrailWaypointSubtype,
    feedback: TrailWaypointFeedback,
    // Location of waypoint itself
    geometry: GeoPoint,
    // Elevation in **meters**
    elevation: number,
}
enum TrailWaypointType {
    Water,
    Camp,
    Natural,
    // transportation
    Trans,
    // TODO: Not sure if these should be here
    Toilet,
    Shower,
}
type TrailWaypointSubtype = WaterSubtype || CampSubtype || NaturalSubtype || TransSubtype;
enum WaterSubtype {
    // Natural LineString water source
    Stream,
    // Natural polygon water source
    Lake,
    // Natural point water source
    Spring,
    // non-natural water source that must be refilled.
    Cache,
    // an always?-running man-made water source. Doesn't need to be refilled,
    // but may sometimes be turned off.
    Faucet
}
enum CampSubtype {
    // wilderness campsite
    campsite,
    // designated campground with multiple sites
    campground,
    // fully enclosed shelter
    enclosedShelter,
    // shelter that is not fully enclosed
    unenclosedShelter,
}
enum NaturalSubtype {
    Pass,
    Peak,
}
enum TransSubtype {
    Highway,
    PavedRoad,
    DirtRoad,
    TrailJunction,
}
type TrailWaypointFeedback = WaterFeedback || CampFeedback || DefaultFeedback;
type WaterFeedback = StreamFeedback || LakeFeedback || SpringFeedback || CacheFeedback || FaucetFeedback;
interface StreamFeedback extends DefaultFeedback {

}
interface LakeFeedback extends DefaultFeedback {

}
interface SpringFeedback extends DefaultFeedback {

}
interface CacheFeedback extends DefaultFeedback {

}
interface FaucetFeedback extends DefaultFeedback {

}
interface CampFeedback extends DefaultFeedback {

}
interface StreamFeedbackItem {
    date: Date,
    userId: number,
    flowing: Flowing
    waterQuality: WaterQuality
}
interface CampFeedbackItem {
    date: Date,
    userId: number,
    // Number of tent sites the user thinks comfortably fit
    campsiteFits: number,
}
interface HitchFeedbackItem {
    date: Date,
    userId: number,
    // Time reported spent waiting for a hitch
    timeHitching: TimeHitching,
}
enum Flowing {
    flowing
    trickle
    dry
}
enum WaterQuality {
    Great
    Good
    Ok
    Poor
}
enum TimeHitching {
    "<15",
    "15-30",
    "30-45",
    "45-60",
    ">60"
}
```

### User

```ts
interface User {
    // Doesn't have to be their real name
    // Must not include any characters that are invalid in URLs
    name: string,
    // Not sure whether to make this required or not
    email: string,
    // password hashed
    password: string,
}
```

## To Do

- How to name tables so that they're easiest to download for offline usage in Parse. I think Parse generally downloads an entire table. Should all tables be prefixed by `PCT_`?
- strings or numbers for identifiers
- locations for each subwaypoint, but connected when clicked
- How to link trail waypoints to the trail itself? The waypoints can be off trail, but I should probably keep track of the mile marker of the closest trail location?
- Where should you keep waypoint responses? Do you want to separate these from what gets recursively downloaded? On the one hand, it's more data than is needed to show the user the current state, on the other, if you're already downloading the comments, downloading these is not that much more. Maybe make the schema work either way?
