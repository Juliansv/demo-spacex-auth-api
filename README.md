# Django rest api to manage auth and communication with space-x API

## Installation

1. Clone the repository
2. Install the requirements
3. Run the server

```bash
git clone
pip install -r requirements.txt
python manage.py runserver
```

## Endpoints

### Auth

-   /signup

```json
{
	"first_name": "name",
	"last_name": "last name",
	"username": "username@example.com",
	"password": "Xxxxx12345"
}
```

-   /login

```json
{
	"username": "username",
	"password": "password"
}
```

-   /loggedIn (GET)

```
Authorization Token <token>
```

### SpaceX

-   /get_missions_data (GET)

```
Authorization Token <token>
```

## Usage

1. Register a user
2. Login
3. Use the token to access the SpaceX API
