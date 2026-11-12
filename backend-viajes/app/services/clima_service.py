
import httpx

from app.core.config import settings
from app.repositories.ciudad_repository import CiudadRepository


class ClimaService:

    API_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, db):
        self.ciudad_repository = CiudadRepository(db)

    def obtener_clima(self, ciudad_id: int) -> dict:

        ciudad = self.ciudad_repository.get_by_id(ciudad_id)

        if ciudad is None:
            raise ValueError("CITY_NOT_FOUND")

        if ciudad.latitud is None or ciudad.longitud is None:
            raise ValueError("CITY_COORDINATES_NOT_FOUND")

        try:
            response = httpx.get(
                self.API_URL,
                params={
                    "lat": ciudad.latitud,
                    "lon": ciudad.longitud,
                    "units": "metric",
                    "lang": "es",
                    "appid": settings.OPENWEATHER_API_KEY,
                },
                timeout=10.0,
            )

            response.raise_for_status()

            data = response.json()

            temperatura = data.get("main", {}).get("temp")
            condiciones = data.get("weather", [])

            if temperatura is None or not condiciones:
                raise ValueError("EXTERNAL_API_ERROR")

            descripcion = condiciones[0].get("description")

            if not isinstance(temperatura, (int, float)):
                raise ValueError("EXTERNAL_API_ERROR")

            if not isinstance(descripcion, str) or not descripcion:
                raise ValueError("EXTERNAL_API_ERROR")

            return {
                "ciudad_id": ciudad.id,
                "ciudad": ciudad.nombre,
                "temperatura": temperatura,
                "unidad": "°C",
                "descripcion": descripcion,
            }

        except httpx.TimeoutException:
            raise ValueError("EXTERNAL_API_TIMEOUT")

        except httpx.HTTPError:
            raise ValueError("EXTERNAL_API_ERROR")

        except (ValueError, TypeError, KeyError):
            raise ValueError("EXTERNAL_API_ERROR")
