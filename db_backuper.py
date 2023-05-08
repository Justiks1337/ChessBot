import yadisk
from config import yadisk_jwt

yandexdisk = yadisk.YaDisk(token=yadisk_jwt)


def backuper():
    """
    Метод backuper() отвечает за бекап БД на яндекс диск

    Ничего в себя не принимает

    :return: Null
    """
    yandexdisk.upload(yadisk_jwt, '/ShopDB', overwrite=True)