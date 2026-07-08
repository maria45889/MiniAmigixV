from unittest.mock import patch

from django.test import SimpleTestCase

from apps.clima.views import _get_coordinates_from_city


class ClimaGeocodingTests(SimpleTestCase):
    @patch("apps.clima.views.requests.get")
    def test_get_coordinates_from_city_uses_open_meteo_geocoding(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "results": [
                {
                    "latitude": -0.22985,
                    "longitude": -78.52495,
                    "name": "Quito",
                    "country": "Ecuador",
                }
            ]
        }

        lat, lon, nombre, pais = _get_coordinates_from_city("Quito")

        self.assertEqual(lat, -0.22985)
        self.assertEqual(lon, -78.52495)
        self.assertEqual(nombre, "Quito")
        self.assertEqual(pais, "Ecuador")
        self.assertEqual(mock_get.call_args.kwargs["params"]["name"], "Quito")
