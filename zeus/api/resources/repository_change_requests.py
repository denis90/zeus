from flask import request
from sqlalchemy.orm import joinedload

from zeus import auth
from zeus.config import db
from zeus.models import Author, ChangeRequest, Email, Repository

from .base_repository import BaseRepositoryResource
from ..schemas import ChangeRequestSchema

change_requests_schema = ChangeRequestSchema(many=True, strict=True)


class RepositoryChangeRequestsResource(BaseRepositoryResource):
    def select_resurce_for_update(self):
        return False

    def get(self, repo: Repository):
        """
        Return a list of change requests for the given repository.
        """
        user = auth.get_current_user()

        query = ChangeRequest.query.options(
            joinedload('parent_revision'),
            joinedload('author'),
        ).filter(
            ChangeRequest.repository_id == repo.id,
        ).order_by(ChangeRequest.number.desc())
        show = request.args.get('show')
        if show == 'mine':
            query = query.filter(
                ChangeRequest.author_id.in_(
                    db.session.query(Author.id).filter(Author.email.in_(
                        db.session.query(Email.email).filter(
                            Email.user_id == user.id
                        )
                    ))
                )
            )

        return self.paginate_with_schema(change_requests_schema, query)
