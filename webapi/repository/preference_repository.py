from webapi.repository.model.dim_group import DimGroup
from webapi.repository.model.user_group import UserGroupMap
from webapi.repository.db import db
from sqlalchemy import or_

class GroupService:
    def add_group(self, group_name,group_description, user_id):
        try:
            # Create a new group and set isDefault to False
            new_group = DimGroup(group_name=group_name, description = group_description, is_default=False)
            db.session.add(new_group)
            db.session.commit()
            group_id = new_group.group_id
            message = "Group created successfully."

            # Map the user to the group
            user_group_map = UserGroupMap(user_id=user_id, group_id=group_id)
            db.session.add(user_group_map)
            db.session.commit()

            return {"message": message, "group_id": group_id, "map_id": user_group_map.id}
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}

    def get_groups(self, user_id):
        try:
            user_groups = db.session.query(DimGroup).filter(
            or_(
                DimGroup.is_default == True,  # Include default groups
                DimGroup.group_id.in_(
                    db.session.query(UserGroupMap.group_id).filter(
                        UserGroupMap.user_id == user_id
                    ).subquery()
                )
            )
        ).all()

            if user_groups:
                return {"user_id": user_id, "groups": [{"group_name": group.group_name,"description": group.description  }for group in user_groups]}
            else:
                return {"message": "User is not mapped to any default groups."}
        except Exception as e:
            return {"error": str(e)}
        
    def delete_group(self, user_id, group_id):
        try:
            # Fetch the user-group mapping
            user_group_map = UserGroupMap.query.filter_by(user_id=user_id, group_id=group_id).first()

            if not user_group_map:
                return {"error": "User is not mapped to this group."}

            # Delete the user-group mapping
            db.session.delete(user_group_map)

            # Delete the group itself
            group_to_delete = DimGroup.query.filter_by(group_id=group_id).first()
            if group_to_delete:
                db.session.delete(group_to_delete)

            # Commit the transaction
            db.session.commit()

            return {"message": "group removed successfully."}

        except Exception as e:
            # Rollback in case of an error
            db.session.rollback()
            return {"error": str(e)}

    def edit_group(self, user_id, group_id, group_name, group_description):
        try:
            # Fetch the group by group_id
            group = DimGroup.query.filter_by(group_id=group_id).first()

            if not group:
                return {"error": "Group not found."}

            # Update the group details
            group.group_name = group_name
            group.description = group_description

            # Commit the changes to the database
            db.session.commit()

            return {"message": "Group updated successfully."}

        except Exception as e:
            # Rollback in case of an error
            db.session.rollback()
            return {"error": str(e)}