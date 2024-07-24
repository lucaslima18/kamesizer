from sqlmodel import select, or_, and_

from src.libs.db.session_manager import instance_session
from src.shared.utils.log_handler import LogHandler
from .ext import ImageAlreadyExists
from .models import Images

logger = LogHandler()


class ImageRepository:
    @staticmethod
    def create_image(image: Images):
        try:
            with instance_session() as session:
                existent_image = session.exec(
                    select(Images).where(Images.image_name == image.image_name)
                ).first()
                if existent_image:
                    raise ImageAlreadyExists("Font already exist!")
                else:
                    new_image = Images.model_validate(image)
                    session.add(new_image)
                    session.commit()
                    session.close()

                    logger.info(f"New image {new_image.image_name} added!")

                return new_image

        except Exception as err:
            logger.error(err)

    @staticmethod
    def get_status_by_name(image_name: str):
        try:
            with instance_session() as session:
                return (
                    session.exec(select(Images).where(Images.image_name == image_name))
                    .first()
                    .resize_status
                )

        except Exception as err:
            # TODO: doing a custom error FontNotFound
            logger.error(err)

    @staticmethod
    def get_by_name(image_name: str):
        try:
            with instance_session() as session:
                return (
                    session.exec(select(Images).where(Images.image_name == image_name))
                    .first()
                )

        except Exception as err:
            # TODO: doing a custom error FontNotFound
            logger.error(err)

    @staticmethod
    def update_resize_status(image_name: str, resize_status: str):
        with instance_session() as session:
            existent_image = session.exec(
                select(Images).where(Images.image_name == image_name)
            ).first()

            if not existent_image:
                logger.error("file not exists")

            existent_image.resize_status = resize_status
            session.add(existent_image)
            session.commit()
            session.close()

            logger.info(
                f"The image {image_name} has been update status to {resize_status}!"
            )
