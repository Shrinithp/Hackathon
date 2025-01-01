from webapi.repository.model.dim_group import DimGroup
from webapi.repository.model.user_group import UserGroupMap
from webapi.repository.db import db

class GroupService:
    def add_group(self, group_name, user_id):
        try:
            # Check if the group already exists
            group = DimGroup.query.filter_by(group_name=group_name, is_deleted=False).first()
            
            if group:
                group_id = group.group_id
                message = "Group already exists. User mapped to the existing group."
            else:
                # Create a new group and set isDefault to False
                new_group = DimGroup(group_name=group_name, isDefault=False)
                db.session.add(new_group)
                db.session.commit()
                group_id = new_group.group_id
                message = "New group created and user mapped to the new group."

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
            # Query to get only the groups where isDefault is True
            user_groups = db.session.query(DimGroup).join(UserGroupMap).filter(
                UserGroupMap.user_id == user_id,
                DimGroup.isDefault == True  # Only fetch groups that are default
            ).all()

            if user_groups:
                return {"user_id": user_id, "groups": [group.group_name for group in user_groups]}
            else:
                return {"message": "User is not mapped to any default groups."}
        except Exception as e:
            return {"error": str(e)}
        
    def delete_user_from_group(self, user_id, group_id):
        try:
            # Find the user-group mapping
            user_group_map = UserGroupMap.query.filter_by(user_id=user_id, group_id=group_id).first()
            
            if not user_group_map:
                return {"error": "User is not mapped to this group."}
            
            # Delete the user from the group
            db.session.delete(user_group_map)
            db.session.commit()

            return {"message": "User successfully removed from the group."}
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}
