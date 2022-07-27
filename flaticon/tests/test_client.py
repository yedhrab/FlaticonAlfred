from pytest import fixture, mark

from ..client import Client

pytestmark = mark.asyncio


@fixture
def client() -> Client:
    return Client()


async def test_download(client: Client):
    images = await client.search_for_images("cat", count=2)
    image_paths = [await client.download_image(image) for image in images]
    assert image_paths
