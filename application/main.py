from sanic import Sanic, Blueprint

from accounts.dependiences import accounts_service
from accounts.routers import bp_accounts
from payments.dependiences import payments_service
from payments.routers import bp_payments
from users.dependiences import users_service
from users.routers import bp_users, bp_auth
from users.utils import JWTTokenService
from utils.json_encoder import dumps


app = Sanic("PaymentsApp", dumps=dumps)
app.ext.openapi.add_security_scheme(
    "token",
    "http",
    scheme="bearer",
    bearer_format="JWT",
)

routers = Blueprint.group(
    bp_auth, bp_users, bp_accounts, bp_payments, version=1
)

app.blueprint(routers)


@app.before_server_start
async def setup_dependencies(app, _):
    app.ctx.accounts_service = accounts_service()
    app.ctx.payments_service = payments_service()
    app.ctx.users_service = users_service()
    app.ctx.token_service = JWTTokenService
