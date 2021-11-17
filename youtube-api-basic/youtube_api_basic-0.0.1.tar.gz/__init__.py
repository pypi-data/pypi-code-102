import bs4
import requests

class YoutubeAPI:
    def __init__(self):
        self.base_url = 'https://www.youtube.com'
        self.search_url = self.base_url + '/results'
        self.video_url = self.base_url + '/watch'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52'
        }

    def search(self, query):
        params = {
            'search_query': query
        }
        response = requests.get(self.search_url, params=params, headers=self.headers)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', {'class': 'yt-lockup-content'})
        videos = []
        for result in results:
            title = result.find('a', {'class': 'yt-uix-tile-link'})['title']
            video_id = result.find('a', {'class': 'yt-uix-tile-link'})['href'].split('=')[1]
            videos.append({
                'title': title,
                'video_id': video_id
            })
        return videos

    def get_video_info(self, video_id):
        params = {
            'v': video_id
        }
        response = requests.get(self.video_url, params=params, headers=self.headers)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        title = soup.find('span', {'id': 'eow-title'}).text
        views = soup.find('div', {'class': 'watch-view-count'}).text.split(' ')[0]
        return {
            'title': title,
            'views': views
        }