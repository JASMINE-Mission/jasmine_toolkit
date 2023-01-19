# 座標系

```uml
@startuml

SatellitePosition ..> Earth

class SatellitePosition {
  + x
  + y
  + z
  + vx
  + vy
  + vz
  + to_heliocentric(date_time):HeliocentricPosition
}

class HeliocentricPosition {
  + x
  + y
  + z
  + vx
  + vy
  + vz
}

class ICRS {
  + α
  + δ
  + μα
  + μδ
  + π
  + tx
  + to_topocentric(観測者の太陽中心座標:HeliocentricPosition) : TopocentricCoordinate
  + change_date(date_time) :  ICRS
}

class TopocentricCoordinate {
  + α
  + δ
  + μα
  + μδ
  + π
  + tx
}

class Earth {
  + {static} location(date_time) : HeliocentricPosition
}

@enduml
```
