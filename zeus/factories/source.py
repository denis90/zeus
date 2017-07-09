import factory

from zeus import models

from .types import GUIDFactory


class SourceFactory(factory.Factory):
    id = GUIDFactory()
    revision = factory.SubFactory('zeus.factories.RevisionFactory')
    date_created = factory.Faker('date_time')

    # automatically populated from revision
    repository = factory.SelfAttribute('revision.repository')
    repository_id = factory.SelfAttribute('revision.repository_id')
    revision_sha = factory.SelfAttribute('revision.sha')

    class Meta:
        model = models.Source
