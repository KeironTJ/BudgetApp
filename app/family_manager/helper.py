from app import db
from app.models import Family, FamilyMembers
from flask import flash

def create_or_join_family(user, create_or_join, family_name=None, invitation_code=None):
    """
    Handles the logic for creating or joining a family.

    Args:
        user (User): The user performing the action.
        create_or_join (str): Either 'create' or 'join'.
        family_name (str): The name of the family to create (if creating).
        invitation_code (str): The invitation code to join a family (if joining).

    Returns:
        bool: True if the operation was successful, False otherwise.
    """

    if create_or_join == 'create':
        if not family_name:
            flash("Family name is required to create a family.", "danger")
            return False

        # Create a new family
        new_family = Family(name=family_name, owner_id=user.id)  # Automatically generates invitation_code
        db.session.add(new_family)
        db.session.commit()

        # Add the user as a member of the family
        family_member = FamilyMembers(user_id=user.id, family_id=new_family.id, role_in_family='owner')
        db.session.add(family_member)
        db.session.commit()

        user.set_active_family(new_family.id)
        db.session.commit()

        flash(f"Family '{family_name}' created successfully! Share this invitation code: {new_family.invitation_code}", "info")
        return True

    elif create_or_join == 'join':
        if not invitation_code:
            flash("Invitation code is required to join a family.", "danger")
            return False

        # Find the family by invitation code
        family = Family.query.filter_by(invitation_code=invitation_code).first()
        if family:
            # Add the user as a member of the family
            family_member = FamilyMembers(user_id=user.id, family_id=family.id)
            db.session.add(family_member)
            db.session.commit()

            user.set_active_family(family.id)
            db.session.commit()

            flash(f"You have successfully joined the '{family.name}' family!", "info")
            return True
        else:
            flash("Invalid invitation code.", "warning")
            return False

    flash("Invalid action. Please choose to create or join a family.", "danger")
    return False