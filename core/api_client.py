import requests
from config.settings import API_BASE_URL, API_KEY, EKSTRAKLASA_LEAGUE_ID

class SportAPIClient:
    def __init__(self):
        self.headers = {
            "X-Api-Key": API_KEY
        }
        self._cache = {}

    def get_standings(self):
        """Pobiera tabelę ligową z uwzględnieniem pamięci podręcznej."""
        cache_key = "standings"
        if cache_key in self._cache:
            print("[CACHE] Pobrano dane tabeli z pamięci podręcznej.")
            return self._cache[cache_key]

        url = f"{API_BASE_URL}/leagues/{EKSTRAKLASA_LEAGUE_ID}/standings"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            self._cache[cache_key] = data
            return data
        else:
            print(f"Blad API (Standings): {response.status_code}")
            return None

    def get_team_details(self, team_id: int):
        """Pobiera statystyki i szczegóły drużyny (z cache)."""
        cache_key = f"team_{team_id}"
        if cache_key in self._cache:
            print(f"[CACHE] Pobrano dane druzyny ID {team_id} z pamięci podręcznej.")
            return self._cache[cache_key]

        url = f"{API_BASE_URL}/teams/{team_id}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            self._cache[cache_key] = data
            return data
        else:
            print(f"Blad API (Team): {response.status_code}")
            return None