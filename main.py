from alfred import AlfredAPI, AlfredResult
from flaticon import FlatIconAPI


def main():
    query = AlfredAPI.get_query()
    images = FlatIconAPI.search_for_images(query, shape="lineal-color")

    alfred_results: list[AlfredResult] = []
    for image in images:
        image_path = str(image.download(foldername=query))
        image_info = f"{image.pack} | {image.downloads}"
        alfred_result = AlfredAPI.to_result(image.name, image_info, image_path, image_path)
        alfred_results.append(alfred_result)

    if alfred_results:
        alfred_response = AlfredAPI.to_response(alfred_results)
        print(alfred_response)
    else:
        alfred_result = AlfredAPI.to_result(
            f"'{query}' not found",
            f"Sorry we couldn't find any matches for '{query}' icons",
            icon_path="images/not-found.png"
        )
        print(AlfredAPI.to_response([alfred_result]))


if __name__ == "__main__":
    main()
