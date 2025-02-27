### User types:
- Unauthorized user/Public directory viewer
- Authenticated team member user
- Sysadmin user

### Use Cases:
##### Member of public viewing team composition
- Can visit web address
- Greeted with a directory of list of members organized by team
- Can only see information that is marked as publicly viewable
- Cannot modify any data in any way

##### Fellow team members viewing team contact info
- Greeted by public directory
	- If they are only trying to view publicly available info, this need is satisfied
- Clicks into authentication flow
- Authenticates via authentication flow
- They are taken to the directory which now includes information that is only viewable to authenticated team members

##### Team members submitting forms for user creation
- Greeted by public directory
- Authenticates via authentication flow
- Clicks into a form submission flow only available to authenticated team members
	- Displays previous form submissions and their status (ability to filter out approved, fully completed form submissions)
	- Option to resume a previously saved form submission attempt in progress
	- Option to create new form submission attempt
- Upon creating new form submission attempting or resuming one ->
- Presented with HTML form page, filled with previously saved information if applicable
- Able to fill in form progressively and the progress is saved to the backend periodically and/or manually via a save button
- Performs any kind of applicable validation to the fields (valid email address, valid telephone number, all fields required are filled)
	- Provides visual feedback if there is something about the field that is not admissible
- If validation passes
	- Able to click to submit form for approval

##### Team members updating their own personal information
- Precondition: authenticated team user
- Team members can view their own profile
- Team members can add and update personal information freely
	- Can impose some kind of minimums to user profiles
		- eg. must have at least 1 valid email address on record
- Users can toggle the public visibility of any of their fields (including their membership?)
- Users must request approval to change their name(?)

##### Sysadmins approving and executing user creation from form submission
- Greeted by public directory
- Authenticates via authentication flow
- Clicks into a form submission flow only available to authenticated team members
- Sysadmins can see all forms in progress
- Sysadmins have an inbox of unapproved, submitted forms
- Sysadmins can view the submitted forms details
	- Could go the route of the fields being read-only and requiring communication with the form submitter to alter the fields
	- Could go the route of requiring to click a button to make the field editable before being able to alter the fields; could notify form submitter that there were last minute changes to the form data
	- Could go the route of not impeding the sysadmin from modifying fields and requiring formal disclosure from this system

##### Sysadmins centrally managing membership and integrations with other team collaboration tools
- Greeted by public directory
- Authenticates via authentication flow
- Sysadmins have the ability to remove team members from the directory
- Sysadmin asked to confirm removal
- Team members marked for removal will be scheduled for complete removal in (n days: 7?), mistakes happen
- Team members marked for removal, all their info is marked private (non-public, possibly only sysadmin visible)
- Team members marked for removal trigger removal from any integrations (after n days as well?)

##### Directory Database Audit trail
- Authenticated sysadmin, or via database backend
- Able to access an audit log showing history of all modifications to the database records
- Records can be periodically cleaned/backed up