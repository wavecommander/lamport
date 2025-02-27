Lamport:
Team directory and (l)ight user m(a)nage(m)ent (port)al

#### High level description of vision
A web portal that provides a publicly accessible team member directory that also allows a level of management with authenticated users and sysadmins.
They are also able to mark information as non-public and only viewable by authenticated team users

#### Scope
Full-stack web app with a DB that will allow CRUD of the team data with authentication, security and privacy considerations.
Easily allows copying out/exporting email addressed in bulk into mailing lists.
Allows for interacting with 3rd party services via API (GitHub and Slack).

Privacy Levels:
0. Public
1. Authenticated Team members
2. Self and Sysadmins
3. {Room for extension to sharing with specific users or other teams}

User permission levels:
1. Regular user
2. Sysadmin
3. {Room for extension}

#### DB Tables
- User identity
	- Given name, surname
	- Full name
	- Preferred addressable name
	- Preferred system username
	- Preferred pronouns
	- Publicly viewable integer
	- Datetime created
	- Datetime updated
- Personal info records
	- Foreign key User record
	- Personal Info type - Enum
		- Email
		- Phone number
		- Address
		- Institution/Organizational affiliation
		- Organizational title or position
		- Profile image URL/src
		- URL (personal page, LinkedIn)
		- Other, descriptive
	- Publicly viewable/Privacy - Integer
	- Datetime created
	- Datetime updated
- Integrations Caching table
	- Updated on integration activity + hourly(?)
	- Foreign key User record
	- Integration type - Enum
		- GitHub
		- Slack
	- API specific info
		- User id
		- Account activation status
		- Permissions and membership info
- Form submission attempts
	- PK ID
	- Submitter
	- Current Status
	- Approver (can be null if not approved)
	- Datetime creation
- Form submission change records
	- FK Form submission attempt ID
	- Form submission ID
	- New state
	- Datetime of state change

##### Form States
- Incomplete/Saved progress
- Submitted/Waiting review
- Rejected/Request for changes
- Approved
- Executed/Marked completed

##### Benefits of chosen architecture
- Decoupled team membership and identity from individual contact methods and pieces of personal info
- Fine grained public/private toggling for all pieces of personal info for each user to decide and update at any time
- Able to add any number of additional or alternative emails/phone numbers without technical limitation
- Offer flexibility for additional desired field types in the future

#### Future Extensions
- Data backups, reliability concerns
- Offline capability/persistence/caching
- Allow for multiple teams, notions of position and relation between and within teams
- Email system
	- Account creation invitations/confirmations
	- Authentication, TOTP, password resets
- Profile images, file hosting, file size/compression and bandwidth considerations

### Backend
- PostgreSQL DB
- Controller in Python FastAPI? Go?

# UI Frontend
Minimal if any JS dependencies.
Prefer no reliance on NPM packages due to security concerns and manageability
#### Main views
- Publicly viewable directory
- Authentication flow
- Authenticated directory with team-only information
- My in-progress and past form submissions
- Create/Resume form submission
- Update my profile information
- Sysadmin form submission review inbox
- Sysadmin form review details
- Sysadmin update a user profile
- Sysadmin manage 3rd party integrations