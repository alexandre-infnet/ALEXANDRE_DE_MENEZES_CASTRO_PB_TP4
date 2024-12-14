from pydantic import BaseModel


class VehicleData(BaseModel):
    brand: str
    model: str
    year: int
    price: float
    category: str
    traction_type: str
    transmission: str
    seats: int
    fuel_type: str
    city_mpg: float
    highway_mpg: float
    combined_mpg: float
    vehicle_size: str
    maintenance_ease: str