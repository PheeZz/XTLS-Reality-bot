import os
from io import BytesIO

import aiofiles


class GuideImagesLoader:
    def __init__(self):
        self._guide_images_path = "source/data/img/guide"
        self._ios_images_paths = self._get_all_files_into_folder(f"{self._guide_images_path}/ios")
        self._android_images_paths = self._get_all_files_into_folder(
            f"{self._guide_images_path}/android"
        )
        self._pc_images_paths = self._get_all_files_into_folder(f"{self._guide_images_path}/pc")

    def _get_all_files_into_folder(self, folder_path: str) -> list[str]:
        return sorted(
            [
                f"{folder_path}/{file}"
                for file in os.listdir(folder_path)
                if os.path.isfile(f"{folder_path}/{file}")
            ]
        )

    async def get_ios_guide_images(self) -> list[BytesIO]:
        return await self._get_guide_images(self._ios_images_paths)

    async def get_android_guide_images(self) -> list[BytesIO]:
        return await self._get_guide_images(self._android_images_paths)

    async def get_pc_guide_images(self) -> list[BytesIO]:
        return await self._get_guide_images(self._pc_images_paths)

    async def _get_guide_images(self, images_paths: list[str]) -> list[BytesIO]:
        images = []
        for image_path in images_paths:
            async with aiofiles.open(image_path, mode="rb") as image_file:
                image = BytesIO(await image_file.read())
                image.seek(0)
                images.append(image)
        return images
