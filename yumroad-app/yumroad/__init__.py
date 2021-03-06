from flask import Flask, render_template
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.rq import RqIntegration

import rq_dashboard

from webassets.loaders import PythonLoader as PythonAssetsLoader

from yumroad import assets
from yumroad.blueprints.products import product_bp
from yumroad.blueprints.stores import store_bp
from yumroad.blueprints.users import user_bp
from yumroad.blueprints.checkout import checkout_bp
from yumroad.blueprints.landing import landing_bp
from yumroad.blueprints.rq_dashboard import rq_blueprint
from yumroad.config import configurations
from yumroad.extensions import (csrf, db, migrate, mail,
                                login_manager, checkout,
                                assets_env, rq2, debug_toolbar,
                                cache)

# We need this line for alembic to discover the models.
import yumroad.models  # noqa: F401

def create_app(environment_name='dev'):
    app = Flask(__name__)
    config = configurations[environment_name]
    app.config.from_object(config)
    db.init_app(app)
    csrf.init_app(app)
    # need render_as_batch to correctly generate migrations for sqlite
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    mail.init_app(app)
    checkout.init_app(app)
    assets_env.init_app(app)
    rq2.init_app(app)
    debug_toolbar.init_app(app)
    cache.init_app(app)

    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    if app.config["SENTRY_DSN"]: # pragma: no cover
        sentry_sdk.init(
            dsn=app.config["SENTRY_DSN"],
            integrations=[FlaskIntegration(), SqlalchemyIntegration(), RqIntegration()]
        )

    @app.errorhandler(401)
    def unauthorized_error(error):
        return render_template('errors/401.html'), 401 # pragma: no cover

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500  # pragma: no cover

    app.register_blueprint(product_bp, url_prefix='/product')
    app.register_blueprint(store_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(landing_bp)

    # Admin tools
    app.register_blueprint(rq_blueprint, url_prefix="/rq")
    csrf.exempt(rq_blueprint)

    return app

# FLASK_DEBUG=true FLASK_APP="yumroad:create_app('dev')" flask run
