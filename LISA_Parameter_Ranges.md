
# LISA Class Parameter Ranges

The ranges of values for the parameters in the `LISA` class and its methods depend on the physical properties of the LiDAR system, atmospheric conditions, and the augmentation type. Below is a breakdown of the key parameters and their typical ranges:

## Parameters in the LISA Class Constructor

| Parameter     | Description                                             | Typical Range                                                  |
|---------------|---------------------------------------------------------|----------------------------------------------------------------|
| `m`           | Refractive index contrast                              | 1.0 to 1.6 (e.g., 1.328 for water, 1.3031 for ice)             |
| `lam`         | Wavelength of the LiDAR system (in nm)                 | 800 to 1550 (e.g., 905 nm for near-infrared LiDAR)            |
| `rmax`        | Maximum LiDAR range (in meters)                        | 50 to 500 (e.g., 200 m)                                       |
| `rmin`        | Minimum LiDAR range (in meters)                        | 0.5 to 5 (e.g., 1.5 m)                                        |
| `bdiv`        | Beam divergence angle (in radians)                     | 1e-4 to 1e-2 (e.g., 3e-3 rad)                                 |
| `dst`         | Minimum droplet diameter to be sampled (in mm)         | 0.01 to 0.5 (e.g., 0.05 mm)                                   |
| `dR`          | Range accuracy (in meters)                             | 0.01 to 0.1 (e.g., 0.09 m)                                    |
| `saved_model` | Whether to use precomputed Mie coefficients            | Boolean                                                       |
| `atm_model`   | Atmospheric model type ('rain', 'snow', 'fog', etc.)  | One of the supported models (e.g., 'rain', 'snow', 'chu_hogg_fog') |
| `mode`        | LiDAR return mode                                      | 'strongest' or 'last'                                        |

## Rain Augmentation Parameters

| Parameter | Description                             | Typical Range                                                      |
|-----------|-----------------------------------------|----------------------------------------------------------------------|
| `Rr`      | Rain rate (in mm/hr)                   | 0.1 to 100 (e.g., 10 mm/hr for moderate rain)                      |
| `D`       | Droplet diameter (in mm)               | 0.01 to 10                                                        |
| `Nd`      | Droplet density (in m⁻³ mm⁻¹)          | Depends on `Rr` and `D` (e.g., 8000 * exp(-4.1 * Rr^(-0.21) * D)) |

## Snow Augmentation Parameters

| Parameter | Description                                    | Typical Range                                               |
|-----------|------------------------------------------------|-------------------------------------------------------------|
| `Rr`      | Water-equivalent snow rate (in mm/hr)         | 0.1 to 50                                                  |
| `D`       | Snow particle diameter (in mm)                | 0.1 to 10                                                  |
| `Nd`      | Snow particle density (in m⁻³ mm⁻¹)           | Depends on `Rr` and `D` (e.g., N0 * exp(-lambda * D))     |

## Fog Augmentation Parameters

| Parameter | Description                                    | Typical Range                                              |
|-----------|------------------------------------------------|------------------------------------------------------------|
| `D`       | Droplet diameter (in mm)                      | 0.001 to 0.1                                               |
| `Nd`      | Droplet density (in m⁻³ mm⁻¹)                 | Depends on the fog model (e.g., Nd_haze_coast, Nd_chu_hogg)|
| `alpha`   | Extinction coefficient (in m⁻¹)              | 0.01 to 1.0                                               |

## Extinction and Backscattering Coefficients

| Parameter | Description                            | Typical Range      |
|-----------|----------------------------------------|--------------------|
| `alpha`   | Extinction coefficient (in m⁻¹)       | 0.01 to 1.0        |
| `beta`    | Backscattering coefficient (in m⁻¹)   | 0.001 to 0.1       |

## Beam Properties

| Parameter | Description                                           | Typical Range                                             |
|-----------|-------------------------------------------------------|-----------------------------------------------------------|
| `Db`      | Beam diameter (in mm)                                | Depends on range and beam divergence (1e3 * tan(bdiv) * range) |
| `bvol`    | Beam volume (in m³)                                  | Depends on range and beam divergence ((π/3) * range * (Db/2)²)  |

## Supported Atmospheric Models

| Model                    | Description                                         |
|--------------------------|-----------------------------------------------------|
| `rain`                   | Rain augmentation using Marshall-Palmer distribution |
| `snow`                   | Snow augmentation using Marshall-Gunn distribution  |
| `chu_hogg_fog`           | Fog augmentation using Chu-Hogg distribution        |
| `strong_advection_fog`   | Strong advection fog model                          |
| `moderate_advection_fog` | Moderate advection fog model                        |
