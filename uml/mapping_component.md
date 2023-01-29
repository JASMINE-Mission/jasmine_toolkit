# Mappingのコンポーネント図

```uml
@startuml

allowmixing 

package "astrometry"
package "calibration"
package "centroid" {
  package "epsf"
}
package "common"
package "data" {
    package "filter"
    package "qe"
}
package "datamodel" {
  class Efficiency
}
package "distortion" {
  package "distortion"
  package "model"
}
package "image" {
  package "imagesim"
  package "pixsim"
  package "psf"
}
package "operation" {
  class "PointingPlan"
  class "PointingPlanFactory"
  class EnumPointingMode <<ENUM>>
}

package "pipeline"
package "satellite" {
  package "attitude" {
    package "attitude"
  }
  package "orbit"
  package "telescope" {
    package "ace"
    package "detector"
    package "filter"
    package "optics"
  }
  class Satellite
}
package "utils" {
  class Mapping
  class Parameters
}

@enduml
```
