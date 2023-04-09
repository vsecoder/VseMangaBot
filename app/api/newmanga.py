import aiohttp
import json
import asyncio


class API:
    """
    Python API SDK for NewManga.org
    """
    def __init__(self):
        self._api = 'https://api.newmanga.org/'
        self._storage = 'https://storage.newmanga.org/'
        self._neo = 'https://neo.newmanga.org/'

        self._all_chapters = self._api + 'v3/branches/{}/chapters/all' # paste manga id
        self._all_pages = self._api + 'v3/chapters/{}/pages' # paste chapter id
        self._projects = self._api + 'v2/projects/{}' # paste manga name(slug)

        self._popular = self._api + 'v2/projects/popular?size={}'

        self._search = self._neo + 'catalogue'

        self._image = self._storage + 'origin_proxy/{}/{}/{}' # paste disk name, chapter id and file name

    async def _request(
            self, 
            url: str, 
            method: str = 'GET', 
            data: dict = None, 
            headers: dict = None
        ) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, data=data, headers=headers) as response:
                if response.headers['Content-Type'] == 'image/jpeg':
                    return await response.read()

                return await response.json()

    async def get_popular(self, pages: int = 3) -> dict:
        return (await self._request(self._popular.format(pages)))['items']
    
    async def get_popular_page(self, page) -> dict:
        return (await self._request(self._popular.format(page)))['items'][page-1]
    
    async def search(self, query: str, page: int = 1, size: int = 4) -> dict:
        data = {
            "query": query,
            "pagination": {"page": page, "size": size},
            "sort": {
                "kind":"MATCH", "dir":"DESC"
            },
            "filter": {
                "hidden_projects":[],
                "adult": {"allowed":[]},
                "genres": {"excluded":[], "included":[]},
                "original_status": {"allowed":[]},
                "released_year": {"max":None, "min":None},
                "require_chapters": False,
                "tags": {"excluded":[], "included":[]},
                "translation_status": {"allowed":[]},
                "type": {"allowed":[]}
            }
        }
        return await self._request(
            self._search,
            method='POST',
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
    
    async def get_chapters(self, manga_id: int) -> dict:
        return await self._request(self._all_chapters.format(manga_id))
    
    async def get_pages(self, chapter_id: int) -> dict:
        return await self._request(self._all_pages.format(chapter_id))
    
    async def get_current_page(self, chapter_id: int, page: int) -> dict:
        return (await self.get_pages(chapter_id))['pages'][page-1]
    
    async def get_image(self, disk_name: str, chapter_id: int, file_name: str) -> bytes:
        return await self._request(
            self._image.format(disk_name, chapter_id, file_name)
        )
    
    async def get_image_url(self, disk_name: str, chapter_id: int, file_name: str) -> str:
        return self._image.format(disk_name, chapter_id, file_name)
    
    async def get_manga_info(self, manga_id: int) -> dict:
        return await self._request(self._projects.format(manga_id))

if __name__ == '__main__':
    api = API()
    loop = asyncio.get_event_loop()
    print(loop.run_until_complete(api.get_popular()))
    print(loop.run_until_complete(api.get_popular_page(2)))
    print(loop.run_until_complete(api.search('one piece')))

    print(loop.run_until_complete(api.get_chapters(4765)))

    print(loop.run_until_complete(api.get_pages(78546)))

    print(loop.run_until_complete(api.get_current_page(78546, 1)))

    #print(loop.run_until_complete(api.get_image(
    #    'app_disk2_parsed', 78546, '33_96E00BD71DC3B352ECCCA233DA76D1B3_0.jpg'
    #)))

    print(loop.run_until_complete(api.get_image_url(
        'app_disk2_parsed', 78546, '33_96E00BD71DC3B352ECCCA233DA76D1B3_0.jpg'
    )))

    print(loop.run_until_complete(api.get_manga_info('mushoku-tensei-if-i-get-to-a-parallel-universe-i-ll-bring')))
