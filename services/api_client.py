import requests
from config.settings import API_BASE_URL, API_KEY, EKSTRAKLASA_LEAGUE_ID

class SportAPIClient:
    def __init__(self):
        self.headers = {
            "X-Api-Key": API_KEY
        }
        self._cache = {}

    def get_standings(self):
        """Pobiera tabelę ligową według wzorca sportapi.ai: GET /standings/{league_id}"""
        cache_key = "standings"
        if cache_key in self._cache:
            print("[CACHE] Pobrano dane tabeli z pamięci podręcznej.")
            return self._cache[cache_key]

        url = f"{API_BASE_URL}/standings/{EKSTRAKLASA_LEAGUE_ID}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            self._cache[cache_key] = data
            return data
        else:
            print(f"Błąd API (Standings): {response.status_code} - {response.text}")
            return None

    def get_team_details(self, team_id: int):
        """Pobiera dane drużyny: GET /teams/{id}"""
        cache_key = f"team_{team_id}"
        if cache_key in self._cache:
            print(f"[CACHE] Pobrano dane drużyny ID {team_id} z pamięci podręcznej.")
            return self._cache[cache_key]

        url = f"{API_BASE_URL}/teams/{team_id}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            self._cache[cache_key] = data
            return data
        else:
            print(f"Błąd API (Team): {response.status_code} - {response.text}")
            return None