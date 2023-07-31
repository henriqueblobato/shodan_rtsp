import logging

from sqlalchemy import func

from models.camera import Camera, DatabaseConnection


class CameraManager(DatabaseConnection):

    def insert_into_cameras(self, ip, port, user, password, url, city, country_code, country_name, region_code):
        city = city.replace("'", "").replace('"', '').replace(';', '')
        camera = Camera(ip=ip, port=port, user=user, password=password, url=url, active=False,
                        city=city, country_code=country_code, country_name=country_name, region_code=region_code)
        with self.session as session:
            session.add(camera)
            session.commit()

    def get_random_from_db(self):
        with self.session as session:
            return session.query(Camera).filter(Camera.active == False).order_by(func.random()).all()

    def get_from_db(self):
        with self.session as session:
            return session.query(Camera).filter(Camera.active == False).all()

    def search_on_db(self, ip, port):
        with self.session as session:
            return session.query(Camera).filter(Camera.ip == ip, Camera.port == port).all()

    def update_active_from_db(self, ip, port):
        with self.session as session:
            camera = session.query(Camera).filter(Camera.ip == ip, Camera.port == port).first()
            if not camera:
                logging.debug(f'Camera {ip}:{port} not found')
                return False
            camera.active = True
            session.commit()
            logging.debug(f'Updated {ip}:{port} to active')
            return True

    def set_active(self, camera):
        with self.session as session:
            db_cam = session.query(Camera).filter(Camera.ip == camera.ip, Camera.port == camera.port).first()
            if db_cam:
                db_cam.active = True
                db_cam.url = camera.url
                db_cam.image_b64 = camera.image_b64
                session.commit()
                logging.debug(f'Updated {camera.ip}:{camera.port}')
            else:
                logging.warning(f'Camera {camera.ip}:{camera.port} not found in the database.')

    def update_from_db_values(self, host, port, user, password, rtsp_string, active):
        with self.session as session:
            camera = session.query(Camera).filter(Camera.ip == host, Camera.port == port).first()
            if camera:
                camera.user = user
                camera.password = password
                camera.url = rtsp_string
                camera.active = active
                session.commit()
                logging.debug(f'Updated {host}:{port} with {user}:{password} and {rtsp_string}')

    def get_all_images_from_db(self):
        with self.session as session:
            return session.query(Camera).filter(Camera.active == True).all()