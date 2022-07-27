from asyncio import run

from alfred import Client as AlfredClient
from flaticon import Client as FlatIconClient
from flaticon import OrderBy, Shape


async def main():
    alfred_client = AlfredClient()
    flaticon_client = FlatIconClient()
    image_count = 9 * alfred_client.page_count
    images = await flaticon_client.search_for_images(
        alfred_client.query, shape=Shape.LINEAL_COLOR, order_by=OrderBy.POPULER, count=image_count
    )
    for image in images:
        image_path = str(await flaticon_client.download_image(image))
        image_info = f"{image.pack} | {image.downloads}"
        alfred_client.add_result(
            title=image.name,
            subtitle=image_info,
            icon_path=image_path,
            arg=image_path,
        )

    if not alfred_client.results:
        alfred_client.add_result(
            f"'{alfred_client.query}' not found",
            f"Sorry we couldn't find any matches for '{alfred_client.query}' icons",
            icon_path="not-found.png"
        )
    await flaticon_client.session.close()
    alfred_client.response()


if __name__ == "__main__":
    run(main())
