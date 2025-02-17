from database.interface import session_scope
from database.models import Workspace, UserWorkspaceAssociative, User, Workflow
from database.models.enums import UserWorkspaceStatus, Permission
from typing import Tuple, List
from sqlalchemy import and_, func

class WorkspaceRepository(object):
    def __init__(self):
        pass

    def find_by_name(self, name):
        with session_scope() as session:
            result = session.query(Workspace).filter(Workspace.name == name).first()
            if result:
                session.expunge(result)
        return result

    def delete_all(self):
        with session_scope() as session:
            session.query(Workspace).delete()
            session.flush()

    def update(self, workspace: Workspace) -> Workspace:
        with session_scope() as session:
            saved_workspace = session.query(Workspace).filter(Workspace.id == workspace.id).first()
            if not saved_workspace:
                raise Exception(f"Workspace {workspace.id} not found")
            saved_workspace.name = workspace.name
            saved_workspace.github_access_token = workspace.github_access_token
            session.flush()
            session.expunge(saved_workspace)
        return saved_workspace
    def create(self, workspace: Workspace) -> Workspace:
        with session_scope() as session:
            session.add(workspace)
            session.flush()
            session.refresh(workspace)
            session.expunge(workspace)
        return workspace

    def find_by_id(self, id: int) -> Workspace:
        with session_scope() as session:
            result = session.query(Workspace).filter(Workspace.id == id).first()
            if result:
                session.expunge_all()
        return result

    def find_workspace_users(self, workspace_id: int, page: int, page_size: int):
        """
        SELECT user_workspace_associative.*, "user".*, total_count.count AS count
        FROM user_workspace_associative
        INNER JOIN "user" ON "user".id = user_workspace_associative.user_id
        CROSS JOIN (
            SELECT COUNT(*) AS count
            FROM user_workspace_associative
            WHERE workspace_id=9
        ) AS count
        WHERE workspace_id = 9
        LIMIT 1;
        """
        with session_scope() as session:
            subquery = (
                session.query(func.count())
                .select_from(UserWorkspaceAssociative)
                .filter(and_(UserWorkspaceAssociative.workspace_id == workspace_id, UserWorkspaceAssociative.status!=UserWorkspaceStatus.rejected.value))
                .scalar_subquery()
            )
            query = (
                session.query(UserWorkspaceAssociative, User, subquery.label('count'))
                .join(User, User.id == UserWorkspaceAssociative.user_id)
                .filter(and_(UserWorkspaceAssociative.workspace_id == workspace_id, UserWorkspaceAssociative.status!=UserWorkspaceStatus.rejected.value))
            )
            results = query.paginate(page, page_size)
            if results:
                session.expunge_all()
        return results


    def find_pending_workspace_invite(self, user_id: int, workspace_id: int):
        with session_scope() as session:
            result = session.query(Workspace, UserWorkspaceAssociative)\
                .join(UserWorkspaceAssociative, Workspace.id==UserWorkspaceAssociative.workspace_id)\
                    .filter(and_(UserWorkspaceAssociative.user_id == user_id, UserWorkspaceAssociative.status == 'pending', Workspace.id == workspace_id))\
                        .first()
            if result:
                session.expunge_all()
        return result

    def update_user_workspace_associative_by_ids(self, associative: UserWorkspaceAssociative):
        with session_scope() as session:
            saved_associative = session.query(UserWorkspaceAssociative)\
                .filter(UserWorkspaceAssociative.user_id == associative.user_id)\
                    .filter(UserWorkspaceAssociative.workspace_id == associative.workspace_id)\
                        .first()
            if not saved_associative:
                return None
            saved_associative.status = associative.status
            session.flush()
            session.expunge(saved_associative)
        return saved_associative


    def find_by_id_and_user(self, id: int, user_id: int) -> Workspace:
        with session_scope() as session:
            """
            SELECT workspace.id, workspace.name, workspace.github_access_token, user_workspace_associative.permission
            FROM workspace
            INNER JOIN user_workspace_associative
            ON  user_workspace_associative.workspace_id = workspace.id and user_id=1
            WHERE workspace_id=9;
            """
            query = session.query(
                Workspace.id.label('id'),
                Workspace.name,
                Workspace.github_access_token,
                UserWorkspaceAssociative.permission.label('permission'),
                UserWorkspaceAssociative.status.label('status')
            )\
            .join(UserWorkspaceAssociative, and_(UserWorkspaceAssociative.workspace_id==Workspace.id, UserWorkspaceAssociative.user_id==user_id))\
            .filter(Workspace.id==id)
            result = query.first()
            if result:
                session.expunge_all()
        return result

    def find_by_user_id(self, user_id: int, page: int, page_size: int, return_rejected: bool = True):
        with session_scope() as session:
            query = session.query(Workspace, UserWorkspaceAssociative.permission, UserWorkspaceAssociative.status)\
                .join(UserWorkspaceAssociative)\
                    .filter(UserWorkspaceAssociative.user_id==user_id)
            if not return_rejected:
                query = query.filter(UserWorkspaceAssociative.status!=UserWorkspaceStatus.rejected.value)
            result = query.paginate(page, page_size)
            if result:
                session.expunge_all()
        return result

    def get_all(self) -> list:
        with session_scope() as session:
            results = session.query(Workspace).all()
            if results:
                session.expunge_all()
        return results

    def find_by_id_and_user_id(self, id: int, user_id: int) -> Tuple[Workspace, UserWorkspaceAssociative]:
        with session_scope() as session:
            query = session.query(Workspace.id.label('workspace_id'), Workspace.name, Workspace.github_access_token, UserWorkspaceAssociative.permission.label('permission'), UserWorkspaceAssociative.status.label('status'))\
                .outerjoin(UserWorkspaceAssociative, and_(UserWorkspaceAssociative.workspace_id==id, UserWorkspaceAssociative.user_id==user_id))\
                    .filter(Workspace.id==id)
            result = query.first()
            if result:
                session.expunge_all()
        return result

    def remove_user_from_workspaces(self, user_id: int, workspaces_ids: List[int]):
        with session_scope() as session:
            session.query(UserWorkspaceAssociative)\
                .filter(and_(UserWorkspaceAssociative.user_id==user_id, UserWorkspaceAssociative.workspace_id.in_(workspaces_ids)))\
                    .delete(synchronize_session=False)

    def find_user_workspaces_members_owners_count(self, user_id: int, workspaces_ids: List[int]) -> List:
        """
        SELECT t1.*, t2.members_count, t3.owners_count, COUNT(wf.id) AS total_workflows
        FROM user_workspace_associative AS t1
        INNER JOIN (
            SELECT workspace_id, COUNT(*) AS members_count
            FROM user_workspace_associative
            WHERE user_workspace_associative.workspace_id IN (2)
            GROUP BY workspace_id
        ) AS t2 ON t1.workspace_id = t2.workspace_id
        INNER JOIN (
            SELECT workspace_id, COUNT(*) AS owners_count
            FROM user_workspace_associative
            WHERE user_workspace_associative.workspace_id IN (2)
            AND user_workspace_associative.permission = 'owner'
            GROUP BY workspace_id
        ) AS t3 ON t1.workspace_id = t3.workspace_id
        LEFT JOIN workflow AS wf ON t1.workspace_id = wf.workspace_id
        WHERE t1.user_id = 2
        AND wf.workspace_id = 2
        GROUP BY t1.user_id, t1.workspace_id, t2.members_count, t3.owners_count;
        """
        with session_scope() as session:
            subquery_users = (
                session.query(
                    UserWorkspaceAssociative.workspace_id,
                    func.count('*').label('members_count')
                )
                .filter(UserWorkspaceAssociative.workspace_id.in_(workspaces_ids))
                .group_by(UserWorkspaceAssociative.workspace_id)
                .subquery()
            )

            # Subquery for counting owners in each workspace
            subquery_owners = (
                session.query(
                    UserWorkspaceAssociative.workspace_id,
                    func.count('*').label('owners_count')
                )
                .filter(UserWorkspaceAssociative.workspace_id.in_(workspaces_ids))
                .filter(UserWorkspaceAssociative.permission == 'owner')
                .group_by(UserWorkspaceAssociative.workspace_id)
                .subquery()
            )

            # Main query
            query = (
                session.query(
                    UserWorkspaceAssociative.user_id,
                    UserWorkspaceAssociative.workspace_id,
                    UserWorkspaceAssociative.permission,
                    UserWorkspaceAssociative.status,
                    subquery_users.c.members_count,
                    subquery_owners.c.owners_count,
                    func.count(Workflow.id).label('total_workflows')
                )
                .join(subquery_users, UserWorkspaceAssociative.workspace_id == subquery_users.c.workspace_id)
                .join(subquery_owners, UserWorkspaceAssociative.workspace_id == subquery_owners.c.workspace_id)
                .outerjoin(Workflow, UserWorkspaceAssociative.workspace_id == Workflow.workspace_id)
                .filter(UserWorkspaceAssociative.user_id == user_id)
                .group_by(
                    UserWorkspaceAssociative.user_id,
                    UserWorkspaceAssociative.workspace_id,
                    subquery_users.c.members_count,
                    subquery_owners.c.owners_count
                )
            )
            result = query.all()
            if result:
                session.expunge_all()
        return result

    def find_user_workspaces_members_count(self, user_id: int, workspaces_ids: List[int]) -> List:
        """
        SQL Query:
        SELECT * from user_workspace_associative as t1
        INNER JOIN (
            SELECT workspace_id, COUNT(*) as members_count from user_workspace_associative
            WHERE user_workspace_associative.workspace_id in (ids) GROUP BY workspace_id
            ) as t2
        ON t1.workspace_id=t2.workspace_id
        WHERE t1.user_id=2;
        """
        with session_scope() as session:
            # create a subquery
            subquery = session.query(
                UserWorkspaceAssociative.workspace_id,
                func.count(UserWorkspaceAssociative.workspace_id).label('members_count')
            ).filter(UserWorkspaceAssociative.workspace_id.in_(workspaces_ids))\
                .group_by(UserWorkspaceAssociative.workspace_id).subquery()

            query = session.query(
                UserWorkspaceAssociative.user_id,
                UserWorkspaceAssociative.workspace_id,
                UserWorkspaceAssociative.permission,
                subquery.c.members_count
            ).join(subquery, UserWorkspaceAssociative.workspace_id == subquery.c.workspace_id)\
                .filter(UserWorkspaceAssociative.user_id == user_id)
            result = query.all()
            if result:
                session.expunge_all()
        return result

    def find_by_name_and_user_id(self, name: str, user_id: int):
        with session_scope() as session:
            result = session.query(Workspace)\
                .join(UserWorkspaceAssociative)\
                    .filter(Workspace.name==name)\
                        .filter(UserWorkspaceAssociative.user_id==user_id).first()
            if result:
                session.expunge_all()
        return result


    def delete(self, id: int):
        with session_scope() as session:
            session.query(Workspace).filter(Workspace.id==id).delete()


