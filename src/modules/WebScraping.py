import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


class CarDataScraper:
    def __init__(self, start_range=2020, end_range=2025, brands=None):
        self.start_range = start_range
        self.end_range = end_range
        self.brands = (
            brands
            if brands
            else [
                "Toyota",
                "Jeep",
                "Nissan",
                "Honda",
                "Land Rover",
                "Dodge",
                "Volkswagen",
                "Volvo",
                "Subaru",
                "Audi",
            ]
        )
        self.car_name_selector = "#main-content > div:nth-child(6) > div.col-sm-9.col-xs-12 > table > tbody > tr:nth-child(n) > td > label > a"
        self.car_details_selector = "#main-content > div:nth-child(6) > div.col-sm-9.col-xs-12 > table > tbody > tr:nth-child(n) > td > label > span"
        self.car_range_selector = "#main-content > div:nth-child(6) > div.col-sm-9.col-xs-12 > table > tbody > tr:nth-child(n) > td > div > div.totalRange"
        self.car_combined_selector = "#main-content > div:nth-child(6) > div.col-sm-9.col-xs-12 > table > tbody > tr:nth-child(n) > td.mpg-epa > div > div > table > tbody > tr:nth-child(1) > td.mpg-comb"
        self.car_city_selector = "#main-content > div:nth-child(6) > div.col-sm-9.col-xs-12 > table > tbody > tr:nth-child(n) > td.mpg-epa > div > div > table > tbody > tr:nth-child(2) > td:nth-child(1)"
        self.car_highway_selector = "#main-content > div:nth-child(6) > div.col-sm-9.col-xs-12 > table > tbody > tr:nth-child(n) > td.mpg-epa > div > div > table > tbody > tr:nth-child(2) > td:nth-child(2)"
        self.car_gal_per_mil = "#main-content > div:nth-child(6) > div.col-sm-9.col-xs-12 > table > tbody > tr:nth-child(n) > td.mpg-epa > div > div > table > tbody > tr:nth-child(4) > td"

    def scrape_data(self):
        data = []
        for brand in self.brands:
            for page in range(
                5
            ):  # Iterar pelas páginas, apenas 5 para não pesar o Scraping
                URL = f"https://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&year1={self.start_range}&year2={self.end_range}&cbmk{brand}={brand}&minmsrpsel=0&maxmsrpsel=0&city=0&hwy=0&comb=0&cbvtgasoline=Gasoline&YearSel={self.start_range}-{self.end_range}&make={brand}&mclass=&vfuel=&vtype=Gasoline&trany=&drive=&cyl=&MpgSel=000&sortBy=Comb&Units=&url=SearchServlet&opt=new&minmsrp=0&maxmsrp=0&minmpg=0&maxmpg=0&sCharge=&tCharge=&startstop=&cylDeact=&rowLimit=10&pageno={page}&tabView=0"
                response = requests.get(URL)
                soup = BeautifulSoup(response.text, "html.parser")

                car_names = soup.select(self.car_name_selector)
                car_details = soup.select(self.car_details_selector)
                car_ranges = soup.select(self.car_range_selector)
                car_combined = soup.select(self.car_combined_selector)
                car_city = soup.select(self.car_city_selector)
                car_highway = soup.select(self.car_highway_selector)
                car_gal_per_mil = soup.select(self.car_gal_per_mil)

                for (
                    name,
                    detail,
                    car_range,
                    combined,
                    city,
                    highway,
                    gal_per_mil,
                ) in zip(
                    car_names,
                    car_details,
                    car_ranges,
                    car_combined,
                    car_city,
                    car_highway,
                    car_gal_per_mil,
                ):
                    car_name = name.get_text(strip=True)
                    car_detail = detail.get_text(strip=True)
                    car_range_value = car_range.get_text(strip=True)
                    combined_mpg = combined.get_text(strip=True)
                    city_mpg = city.get_text(strip=True)
                    highway_mpg = highway.get_text(strip=True)
                    car_gal_per_mil = gal_per_mil.get_text(strip=True)

                    year = car_name.split(" ")[0]
                    model = re.sub(r"^\d{4}\s+", "", car_name)

                    cylinders = re.search(r"(\d+)\s*cyl", car_detail)
                    engine_size = re.search(r"(\d+\.\d+)\s*L", car_detail)
                    fuel_type = re.search(
                        r"(Premium Gasoline|Regular Gasoline|Midgrade Gasoline)",
                        car_detail,
                    )
                    car_range_value = re.search(r"(\d+)", car_range_value)

                    cylinders = cylinders.group(1) if cylinders else "N/A"
                    engine_size = engine_size.group(1) if engine_size else "N/A"
                    fuel_type = fuel_type.group(1) if fuel_type else "N/A"
                    car_range_value = (
                        car_range_value.group(1) if car_range_value else "N/A"
                    )

                    data.append(
                        {
                            "Marca do Carro": brand,
                            "Ano do Carro": year,
                            "Cilindros do Carro": cylinders,
                            "Litragem do Motor": engine_size,
                            "Modelo do Carro": model,
                            "Tipo de Gasolina": fuel_type,
                            "Cidade (MPG)": city_mpg,
                            "Rodovia (MPG)": highway_mpg,
                            "Combinado (MPG)": combined_mpg,
                            "Autonomia Total (MPG)": car_range_value,
                            "Galões por Milhas": car_gal_per_mil,
                        }
                    )
        return data

    def save_to_csv(self, filename="cars_data.csv"):
        data = self.scrape_data()
        df = pd.DataFrame(data)
        df.index.name = "Índice"
        df.to_csv(filename, index=False)
        print(df)


if __name__ == "__main__":
    scraper = CarDataScraper()
    scraper.save_to_csv("src/data/cars_data.csv")
