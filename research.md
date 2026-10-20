# Research

## My own Modding Docs

<https://www.subwaybuilder.com/docs/beta/api-reference/trains>

TrackTypes: `light-metro`, `heavy-metro`, `light-rail`, `commuter-rail`, `commuter-rail-diesel`

### Vanilla Reference

Operating Costs - train/hr, car/hr, track/m, station/yr(k)

- `heavy-metro`: 250, 25, 360, 320
- `light-metro`: 180, 20, 280, 200
- `light-rail`: 220, 20, 280, 200
- `commuter-rail`: 500, 35, 300, 320
- `commuter-rail-diesel`: 650, 35, 300, 320

Capital Costs - car(M), track(k), station(M)

- `heavy-metro`: 2.7, 30, 60
- `light-metro`: 2.5, 30, 45
- `light-rail`: 2, 25, 40
- `commuter-rail`: 3.5, 25, 55
- `commuter-rail-diesel`: 3, 19, 50

Train cars:

- `heavy-metro`: 18.4x3.0, 240 pax, 40 seats
- `light-metro`: 19.1x2.9, 200 pax, 64 seats
- `light-rail`: 9.6x2.6, 77 pax, 25 seats

Track parameters - track spacing, track clearance

- `heavy-metro`: 3.8, 1.0
- `light-metro`: 3.8, 1.0
- `light-rail`: 3.2, 1.6
- `commuter-rail`/`commuter-rail-diesel`: 4.3, 1.2

### Side Effects of modifying default trains

Loading into an existing save with different track parameters (especially clearance, spacing) - not an issue, the save literally keeps each track segment's clearance and spacing (at least in beta). So when you load in a mod that modifies that, existing tracks remain exactly the same.

## Train Selections

Uk Sources:

- <https://en.wikipedia.org/wiki/British_railway_rolling_stock#Multiple_units_and_railcars>

### Heavy Metro

### Light Metro

[Frequencies](https://en.wikipedia.org/wiki/Manchester_Metrolink#Frequencies)

44 tph in the core city section?????

- Taking a look at Google Maps on a Sunday at 5 pm, it does seem to be about 20 trams per half hour in both directions (i.e. 20 tphpd)

### Light Rail

Need to set crossing speed limits? Or use the default 35 mph

### Electric Commuter Train

Ingame M9 for reference:

- Accel 0.9, Decel 1.34; max 80 mph
- 106/106 per car; 424-1484 overall capacity (4-14 cars)
- 26 x 3.3 m
- 30 tph
- Turning radii: 88/500 m

Other updatable stats

- Level crossing TPH limit perhaps: set maximum to 20: [RailUKForums](https://www.railforums.co.uk/threads/busiest-level-crossings-in-the-uk-today.229503/)
- Level crossing speed limit: full speed (no changes)

### Diesel Commuter Train

Just gonna be a Sprinter???

Ingame P32 + Comet V for reference:

- Accel 0.49, Decel 1.34; max 80 mph
- 112/112 per car; 448-1568 overall capacity (4-14 cars)
- 26 x 3.3 m
- 30 tph
- Turning radii: 88/500 m

It seems that most British DMUs (at least in the Sprinter and Sprinter-replacement variety) have very similar specs:

- ~70 seats per car
- 75 mph for local/commuter variants (150-158), 90 mph for 158s, 100 mph for most replacement varieties
- Some more specific specs
  - 158 has 0.8m/s2 acceleration
  - Based on [this doc](https://web.archive.org/web/20150121172516/http://barrowmoremrg.co.uk/BRBDocuments/Book220Issue.pdf),
    Turning circles: 150 70m; 154 70m; 156 90m;

What I think I could do, is have the diesel commuter train as a slow, cheap, higher speed, low-capacity commuter system :)

### Mainline infrastructure sizing

- Distance between inner rails, double track: 6 ft (<https://igg.org.uk/rail/2-track/02track3.htm>)
- Loading gauge is approximately 9 ft wide
- This computes to
  - Track spacing (between centrelines): 3.26 m (10'8.5")
  - loading gauge clearance (beyond rail): .65 m

## Custom Acceleration Curves

```plain
heavy-metro: {a0: 1.12, a1: 1.12, v1: 8.5, v2: 17, exponent: 2}
light-metro: {a0: 1.2, a1: 1.15, v1: 12.5, v2: 22, exponent: 2}
commuter-rail: {a0: 0.894, a1: 0.894, v1: 15.65, v2: 15.65, exponent: 1.2}
commuter-rail-diesel: {a0: 0.49, a1: 0.49, v1: 6.5, v2: 15, exponent: 1.7}
```

It seems like:

- The initial ramp up to a0 is predetermined by the game and is not configurable
- Acceleration then changes linearly from a0 to a1; reaches a1 at velocity v1
- Then from v1 to v2 acceleration decreases exponential with the exponent
- Then... I'm not sure.
  - V2 are respectively: 61, 79, 56, 54 kph
  - It could be a linear decrease afterwards (no it definitely doesn't decease to zero)
  - The acceleration-time graphs looks like another exponential decrease afterwards - which could imply linearly decreasing acceleration with velocity? But what rate?

### Davis Equation Coefficients

The Rochard paper [2] shows signification deviations between Armstrong and Swift's equations (empirical obtained from UK trains, specifically EMUs) compared to French (SNCF) and German (Sauthoff) equations.

I could not find a way to access Armstrong and Swift's 1990 British Rail Report, so stuff that is credited to them is copied from works that reference that paper.

Armstrong-Swift coefficients:

```plain
Units: t, kW, m, m^2

A = 6.4 * m_total_trailer_cars
  + 8.0 * m_total_power_cars

B = 0.18 * m_train
  + 1 * n_trailer_cars
  + 0.005 * n_power_carss * p_total

C = 0.6125 * coeff_drag_head * area_cross_section
  + 0.00197 * perimeter * length
  + 0.0021 * perimeter * length_intervehicle_gap * (n_cars - 1)
  + 0.2061 * coeff_drag_bogie * n_bogie
  + 0.2566 * n_pantograph
```

For each vehicle, required parmeters:

- te_initial/accel_initial (for performance calculation)
- p_total
- m_trailer_car
- m_power_car
- n_trailer_cars
- n_power_cars
- length
- length_intervehicle_gap
- coeff_drag_head
  - ~~Based on the SNCF equation for suburban electric trains, and plugging in values from the Class 345, a suitable head/tail drag coefficient is around 0.9~~
    - ~~The equation in question: C (kgf) = 0.0035 S + 0.0041 p \* L / 100 + 0.002 N_panto~~
  - For reference, values Rochard used for the series 100 Shinkansen and Class 373 Eurostar were around 0.07 to 0.075.
- coeff_drag_bogie
  - Rochard: 0.6 is about right for a UK suburban EMU.
- perimeter
- area_cross_section
- n_pantograph
- n_bogie

All masses are empty (tare) masses

Some values are exact, some are estimated based on rolling stock diagrams and drawings, some are estimated based on similar values used by existing equations

#### 2009 Stock

193.2 t

- te_initial/accel_initial: 1.3 m/s^2
- p_total: 24 \* 75 = 1800 kW
- m_trailer_car: 21.6
- m_power_car: 25
- n_trailer_cars: 2
- n_power_cars: 6
- length: 133.275
- length_intervehicle_gap: 0.25
- coeff_drag_head: 0.5
- coeff_drag_bogie: 0.6
- perimeter: 9.2 m
- area_cross_section: 5.9 m^2
- n_pantograph: 0
- n_bogie: 16

A = 1.48, B = 0.0638, C = 0.00840

Power-wheel Efficiency = 0.9

Derived: a0 = 1.3, a1 = 1.29, v1 = 6.4, v2 = 10.6, exponent = 1.11

#### DLR B07

38.2 t

- te_initial/accel_initial: 1.4 m/s^2;
  - 4800 kN TE doesn't seem right
- p_total: 520 kW
- m_trailer_car: 0
- m_power_car: 19.1
- n_trailer_cars: 0
- n_power_cars: 2
- length: 28
- length_intervehicle_gap: 0
  - Because of flush covers between cars
- coeff_drag_head: 0.4
- coeff_drag_bogie: 0.55 (Because smaller?)
- perimeter: 10.4 m
- area_cross_section: 7.6 m^2
- n_pantograph: 0
- n_bogie: 3

A = 0.306, B = 0.0121, C = 0.00464

Power-wheel Efficiency = 0.9

Derived: a0 = 1.4, a1 = 1.38, v1 = 8.7, v2 = 12.8, exponent = 1.23

#### Metrolink M5000

39.6 t

- te_initial/accel_initial: 1.08m/s^2
- p_total: 480 kW
- m_trailer_car: 0
- m_power_car: 19.8
- n_trailer_cars: 0
- n_power_cars: 2
- length: 28.4
- length_intervehicle_gap: 0
  - Because of flush covers between cars
- coeff_drag_head: 0.4
- coeff_drag_bogie: 0.45 (bogie skirts)
- perimeter: 12.5 m
- area_cross_section: 9.6 m^2
- n_pantograph: 1
- n_bogie: 3

A = 0.317, B = 0.0119, C = 0.00682

Power-wheel Efficiency = 0.9

Derived: a0 = 1.08, a1 = 1.06, v1 = 10, v2 = 12.8, exponent = 1.37

#### Class 345

319 t

- te_initial/accel_initial: 1 m/s^2
- p_total: 4400 kW (at rail, 5000 kW total)
- m_trailer_car: 36.5
- m_power_car: 35.1
- n_trailer_cars: 1
- n_power_cars: 8
- length: 204.73
- length_intervehicle_gap: 0.65
- coeff_drag_head: 0.35
- coeff_drag_bogie: 0.6
- perimeter: 11.1 m
- area_cross_section: 9.4 m^2
- n_pantograph: 2
- n_bogie: 18

A = 2.48, B = 0.234, C = 0.0125

Power-wheel Efficiency = 1.0 (4.4 MW is already measured at wheel)

Derived: a0 = 1, a1 = 0.98, v1 = 13.6, v2 = 23.2, exponent = 1.65

#### Class 150

2-car 150/2, using DMS (diagram DP 242)

73.0 t

- te_initial/accel_initial
- p_total: 426 kW
- m_trailer_car: 0
- m_power_car: 36.5
- n_trailer_cars: 0
- n_power_cars: 2
- length: 2 \* 20.06 = 40.1 m
- length_intervehicle_gap: 0.32 m
- coeff_drag_head: 0.7
- coeff_drag_bogie: 0.6
- perimeter: 10.9 m
- area_cross_section: 7.4 m^2
- n_pantograph: 0
- n_bogie: 4

A = 0.584, B = 0.0153, C = 0.00680

Power-wheel Efficiency = 0.8

Derived: a0 = 0.8, a1 = 0.79, v1 = 5.8, v2 = 14, exponent = 1.89

Likely least accurate due to diesel-hydraulic drive

### Sources...?

1. <https://web.archive.org/web/20221205004502/https://www.railtechnical.com/br-class-150> - not currently useful
2. B P Rochard, F Schmid. A review of methods to measure and calculate train resistances. 2000.

## TODOS

[ ] Rename to UK-Vanilla Train Pack?
