from django.test import TestCase
from django.db.utils import IntegrityError
from example.serializers import TrackSerializer, TrackSerializer2, AlbumSerializer, AlbumSerializer2


class ChapterSerializerTests(TestCase):
    def setUp(self):
        self.album_data = {
            'album_name':
            'The Grey Album',
            'artist':
            'Danger Mouse',
            'tracks': [
                {
                    'order': 1,
                    'title': 'Public Service Announcement',
                    'duration': 245
                },
                {
                    'order': 2,
                    'title': 'What More Can I Say',
                    'duration': 264
                },
                {
                    'order': 3,
                    'title': 'Encore',
                    'duration': 159
                },
            ],
        }

    def test_create_album_with_nested_tracks(self):
        serializer = AlbumSerializer(data=self.album_data)
        is_valid = serializer.is_valid()
        self.assertDictEqual(serializer.errors, {})
        self.assertTrue(is_valid)
        self.assertTrue(serializer.save())

    def test_add_track_with_album_failes(self):
        album_serializer = AlbumSerializer(data=self.album_data)
        album_serializer.is_valid()
        album = album_serializer.save()

        data = {
            'order': 4,
            'title': 'December 4th',
            'duration': 220,
            'album': album.id
        }
        serializer = TrackSerializer(data=data)
        is_valid = serializer.is_valid()
        self.assertDictEqual(serializer.errors, {})
        self.assertTrue(is_valid)
        error_msg = 'NOT NULL constraint failed: example_track.album_id'
        with self.assertRaisesMessage(IntegrityError, error_msg):
            serializer.save()

    def test_add_track_with_album_using_serializer2(self):
        album_serializer = AlbumSerializer(data=self.album_data)
        album_serializer.is_valid()
        album = album_serializer.save()

        data = {
            'order': 4,
            'title': 'December 4th',
            'duration': 220,
            'album': album.id
        }
        serializer = TrackSerializer2(data=data)
        is_valid = serializer.is_valid()
        self.assertDictEqual(serializer.errors, {})
        self.assertTrue(is_valid)
        self.assertTrue(serializer.save())

    def test_create_album_with_nested_tracks_using_serializer2_fails(self):
        serializer = AlbumSerializer2(data=self.album_data)
        is_valid = serializer.is_valid()
        self.assertDictEqual(serializer.errors, {
            'tracks': [{
                'album': ['This field is required.']
            }, {
                'album': ['This field is required.']
            }, {
                'album': ['This field is required.']
            }]
        })

        self.assertFalse(is_valid)
        error_msg = 'You cannot call `.save()` on a serializer with invalid data.'
        with self.assertRaisesMessage(AssertionError, error_msg):
            serializer.save()
