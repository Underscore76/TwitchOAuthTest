# Twitch OAuth Client example

Very simple version of getting a request client that'll start the initial login flow, request a token, and then create a auto-refreshing client (using `requests_oauthlib`)

*** TREAT `CLIENT IDS`, `CLIENT SECRETS`, `ANY AND ALL TOKENS` AS PASSWORDS ***

# Usage

1. `pip install -r requirements.txt` (always prefer a new environment/conda/etc but you do you)
2. Copy `.env.example` to `.env` and fill in the details
3. Update whatever scopes you want in the main call
4. Run the code and follow the prompts
   1. It'll ask you to click a link which will bring you to a twitch authorize prompt
   2. After authorizing, you'll get to a dead page (NORMAL). copy the result in the address bar and paste that back into your terminal at the prompt
5. Should print out your tokens, and return a request client that can be used for hitting the twitch api
