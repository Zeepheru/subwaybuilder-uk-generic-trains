def calculate_params(
    p_total,
    m_trailer_car,
    m_power_car,
    n_trailer_cars,
    n_power_cars,
    length,
    length_intervehicle_gap,
    coeff_drag_head,
    coeff_drag_bogie,
    perimeter,
    area_cross_section,
    n_pantograph,
    n_bogie,
):
    m_total_trailer_cars = n_trailer_cars * m_trailer_car
    m_total_power_cars = n_power_cars * m_power_car
    m_train = m_total_trailer_cars + m_total_power_cars

    n_cars = n_trailer_cars + n_power_cars

    A = (6.4 * m_total_trailer_cars) + (8.0 * m_total_power_cars)

    B = (0.18 * m_train) + (1 * n_trailer_cars) + (0.005 * n_power_cars * p_total)

    C = (
        (0.6125 * coeff_drag_head * area_cross_section)
        + (0.00197 * perimeter * length)
        + (0.0021 * perimeter * length_intervehicle_gap * (n_cars - 1))
        + (0.2061 * coeff_drag_bogie * n_bogie)
        + (0.2566 * n_pantograph)
    )

    A /= 1000
    B /= 1000
    C /= 1000

    print("Calculated values (for R in kN):" + f"\nA: {A}" + f"\nB: {B}" + f"\nC: {C}")

    return A, B, C


if __name__ == "__main__":
    # calculate_params(
    #     p_total=213,
    #     m_trailer_car=0,
    #     m_power_car=36.5,
    #     n_trailer_cars=0,
    #     n_power_cars=2,
    #     length=40.1,
    #     length_intervehicle_gap=0.32,
    #     coeff_drag_head=1.2,
    #     coeff_drag_bogie=0.6,
    #     perimeter=10.9,
    #     area_cross_section=7.4,
    #     n_pantograph=0,
    #     n_bogie=4,
    # )

    # Class 373 Sanity Check
    calculate_params(
        p_total=12000,
        m_trailer_car=60.8,
        m_power_car=68.5,
        n_trailer_cars=12,
        n_power_cars=2,
        length=394,
        length_intervehicle_gap=0.32,
        coeff_drag_head=0.07,
        coeff_drag_bogie=0.5,
        perimeter=11.24,
        area_cross_section=8.9,
        n_pantograph=2,
        n_bogie=28,
    )
