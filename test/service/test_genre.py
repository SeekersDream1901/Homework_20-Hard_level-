from unittest.mock import MagicMock

import pytest

from dao.model.genre import Genre
from dao.genre import GenreDAO
from service.genre import GenreService


@pytest.fixture()
def genres_dao():
    genres_dao = GenreDAO(None)

    genre_1 = Genre(id=1, name='Ужасы')
    genre_2 = Genre(id=2, name='Комедии')
    genre_3 = Genre(id=3, name='Триллеры')
    genre_4 = Genre(id=4, name='Мультфильмы')
    genre_5 = Genre(id=5, name='Детективы')

    genres_dao.get_one = MagicMock(return_value=genre_1)
    genres_dao.get_all = MagicMock(return_value=[genre_5, genre_4, genre_3, genre_2, genre_1])
    genres_dao.create = MagicMock(return_value=Genre(id=6))
    genres_dao.delete = MagicMock(return_value=Genre(id=3))
    genres_dao.update = MagicMock(return_value=genre_3)

    return genres_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genres_dao):
        self.genre_service = GenreService(dao=genres_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)

        assert genre is not None
        assert genre.id is not None
        assert genre.name == 'Ужасы'

    def test_get_all(self):
        genres = self.genre_service.get_all()

        assert len(genres) > 0
        assert len(genres) == 5

    def test_create(self):
        data = {
            "name": 'Биография'
        }

        genre = self.genre_service.create(data)

        assert genre.id is not None
        assert genre.id == 6

    def test_delete(self):
        genre = self.genre_service.delete(3)

        assert genre is None

    def test_update(self):
        data = {
            "id": 3,
            "name": 'Бред)'
        }
        genre = self.genre_service.update(data)
        assert genre is None

    def test_partially_update(self):
        data = {
            "id": 3,
            "name": 'Фантастика'
        }

        genre = self.genre_service.partially_update(data)

        assert genre is None